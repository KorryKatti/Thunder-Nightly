import { el, formatNumber, escapeHtml } from '../utils.js';
import { navigate } from '../router.js';
import { renderURLBar } from '../components/urlbar.js';
import { fetchRepoInfo, fetchReadme, installApp, openExternal } from '../api.js';
import { showToast } from '../components/toasts.js';
import { marked } from 'marked';

export function renderAppDetail(container, encodedURL) {
    container.innerHTML = '';

    const url = decodeURIComponent(encodedURL);

    // URL bar at top
    const urlSection = el('div', { className: 'detail-url-section' });
    renderURLBar(urlSection, {
        onSubmit: (newUrl) => navigate(`/app/${encodeURIComponent(newUrl)}`),
        currentURL: url
    });
    container.appendChild(urlSection);

    // Loading state
    const contentArea = el('div', { className: 'detail-content', id: 'detail-content' });
    contentArea.appendChild(el('div', { className: 'detail-loading' }, [
        el('div', { className: 'spinner' }),
        el('span', { text: 'Loading repository...' })
    ]));
    container.appendChild(contentArea);

    // Fetch data
    loadRepoData(contentArea, url);
}

async function loadRepoData(container, url) {
    try {
        console.log('Loading repo data for:', url);
        const repoInfo = await fetchRepoInfo(url);
        console.log('Repo info type:', typeof repoInfo, 'keys:', repoInfo ? Object.keys(repoInfo) : 'null');
        console.log('Full repoInfo:', JSON.stringify(repoInfo, null, 2));

        if (!repoInfo || typeof repoInfo !== 'object') {
            throw new Error('Invalid repository data received');
        }

        let readme = '';
        try {
            readme = await fetchReadme(url);
        } catch (readmeErr) {
            console.warn('README fetch failed (non-fatal):', readmeErr);
        }

        container.innerHTML = '';
        renderRepoPage(container, repoInfo, readme, url);
    } catch (e) {
        console.error('Failed to load repo:', e);
        container.innerHTML = '';
        container.appendChild(el('div', { className: 'detail-error' }, [
            el('div', { className: 'detail-error-icon', text: '!' }),
            el('h3', { text: 'Failed to load repository' }),
            el('p', { className: 'detail-error-msg', text: String(e) }),
            el('button', {
                className: 'btn btn-secondary',
                text: 'Back to Home',
                onClick: () => navigate('/')
            })
        ]));
    }
}

function renderRepoPage(container, repo, readme, url) {
    // Hero
    const hero = el('div', { className: 'detail-hero' }, [
        el('div', { className: 'detail-hero-bg' }),
        el('div', { className: 'detail-hero-content' }, [
            el('div', { className: 'detail-hero-icon', text: repo.Name.charAt(0).toUpperCase() }),
            el('div', { className: 'detail-hero-info' }, [
                el('p', { className: 'detail-hero-fullname', text: repo.FullName }),
                el('h1', { className: 'detail-hero-name', text: repo.Name }),
                el('p', { className: 'detail-hero-desc', text: repo.Description || 'No description' })
            ])
        ])
    ]);

    // Stats
    const stats = el('div', { className: 'detail-stats' }, [
        createStat('★', formatNumber(repo.Stars), 'Stars'),
        createStat('⑂', formatNumber(repo.Forks), 'Forks'),
        repo.Language ? createStat('●', repo.Language, 'Language') : null,
        repo.LicenseName ? createStat('📄', repo.LicenseName, 'License') : null
    ].filter(Boolean));

    // Actions
    const actions = el('div', { className: 'detail-actions' }, [
        el('button', {
            className: 'btn btn-green btn-lg',
            text: 'Install',
            onClick: async (e) => {
                e.target.disabled = true;
                e.target.textContent = 'Installing...';
                const result = await installApp(url);
                if (result.success) {
                    showToast(`${repo.Name} installed successfully!`, 'success');
                    e.target.textContent = 'Installed';
                } else {
                    showToast('Install failed: ' + result.error, 'error');
                    e.target.disabled = false;
                    e.target.textContent = 'Install';
                }
            }
        }),
        el('button', {
            className: 'btn btn-secondary btn-lg',
            text: 'View on GitHub',
            onClick: () => openExternal(repo.URL)
        })
    ]);

    container.appendChild(hero);
    container.appendChild(stats);
    container.appendChild(actions);

    // README
    if (readme) {
        const readmeContent = el('div', {
            className: 'detail-readme-content markdown-body',
            html: marked.parse(readme)
        });

        // Open external links in system browser
        readmeContent.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link) {
                const href = link.getAttribute('href');
                if (href && (href.startsWith('http://') || href.startsWith('https://'))) {
                    e.preventDefault();
                    openExternal(href);
                }
            }
        });

        const readmeSection = el('div', { className: 'detail-readme' }, [
            el('h2', { className: 'detail-section-title', text: 'README' }),
            readmeContent
        ]);
        container.appendChild(readmeSection);
    }
}

function createStat(icon, value, label) {
    return el('div', { className: 'detail-stat' }, [
        el('span', { className: 'detail-stat-icon', text: icon }),
        el('span', { className: 'detail-stat-value', text: value }),
        el('span', { className: 'detail-stat-label', text: label })
    ]);
}
