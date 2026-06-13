import { el } from '../utils.js';
import { navigate } from '../router.js';
import { renderURLBar } from '../components/urlbar.js';
import { checkUV, installUV } from '../api.js';
import { showToast } from '../components/toasts.js';

export function renderHome(container) {
    container.innerHTML = '';

    const wrapper = el('div', { className: 'home-wrapper' });

    // Hero section
    const hero = el('div', { className: 'home-hero' }, [
        el('div', { className: 'home-hero-icon', html: '⚡' }),
        el('h1', { className: 'home-hero-title', text: 'Thunder' }),
        el('p', { className: 'home-hero-subtitle', text: 'Run any Python app from GitHub instantly' })
    ]);

    // URL input section
    const urlSection = el('div', { className: 'home-url-section' });
    renderURLBar(urlSection, {
        onSubmit: (url) => navigate(`/app/${encodeURIComponent(url)}`)
    });

    // UV status section
    const uvSection = el('div', { className: 'home-uv-section', id: 'uv-status' });
    renderUVStatus(uvSection);

    // Recent URLs (placeholder for future)
    const recentSection = el('div', { className: 'home-recent' }, [
        el('h3', { className: 'home-recent-title', text: 'Quick Links' }),
        el('div', { className: 'home-recent-grid' }, [
            createQuickLink('https://github.com/pypa/hatch', 'Hatch', 'Modern Python project management'),
            createQuickLink('https://github.com/astral-sh/uv', 'uv', 'Fast Python package installer'),
            createQuickLink('https://github.com/jlowin/fastmcp', 'FastMCP', 'Build MCP servers in Python')
        ])
    ]);

    wrapper.appendChild(hero);
    wrapper.appendChild(urlSection);
    wrapper.appendChild(uvSection);
    wrapper.appendChild(recentSection);
    container.appendChild(wrapper);
}

function createQuickLink(url, name, description) {
    return el('div', {
        className: 'home-quicklink',
        onClick: () => navigate(`/app/${encodeURIComponent(url)}`)
    }, [
        el('div', { className: 'home-quicklink-icon', text: name.charAt(0).toUpperCase() }),
        el('div', { className: 'home-quicklink-info' }, [
            el('span', { className: 'home-quicklink-name', text: name }),
            el('span', { className: 'home-quicklink-desc', text: description })
        ])
    ]);
}

async function renderUVStatus(container) {
    container.innerHTML = '';
    container.appendChild(el('div', { className: 'uv-loading', text: 'Checking uv...' }));

    const { installed, version } = await checkUV();

    container.innerHTML = '';

    if (installed) {
        container.appendChild(el('div', { className: 'uv-status uv-installed' }, [
            el('span', { className: 'uv-status-icon', html: '&#10003;' }),
            el('span', { className: 'uv-status-text', html: `<strong>uv</strong> is ready (${version})` })
        ]));
    } else {
        container.appendChild(el('div', { className: 'uv-status uv-missing' }, [
            el('span', { className: 'uv-status-icon', text: '!' }),
            el('span', { className: 'uv-status-text', html: '<strong>uv</strong> is not installed' }),
            el('button', {
                className: 'btn btn-primary btn-sm',
                text: 'Install uv',
                onClick: async (e) => {
                    e.target.disabled = true;
                    e.target.textContent = 'Installing...';
                    const result = await installUV();
                    if (result.success) {
                        showToast('uv installed successfully!', 'success');
                        renderUVStatus(container);
                    } else {
                        showToast('Failed to install uv: ' + result.error, 'error');
                        e.target.disabled = false;
                        e.target.textContent = 'Install uv';
                    }
                }
            })
        ]));
    }
}
