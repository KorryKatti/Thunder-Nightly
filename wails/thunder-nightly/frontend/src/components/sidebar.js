import { el } from '../utils.js';
import { getState, subscribe } from '../state.js';
import { getCurrentPath, navigate } from '../router.js';

const navItems = [
    { id: 'home', label: 'Home', icon: homeIcon(), path: '/' },
    { id: 'settings', label: 'Settings', icon: settingsIcon(), path: '/settings' }
];

function homeIcon() {
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`;
}

function storeIcon() {
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`;
}

function libraryIcon() {
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`;
}

function settingsIcon() {
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`;
}

export function renderSidebar(container) {
    const sidebar = el('nav', { className: 'sidebar' }, [
        el('div', { className: 'sidebar-logo' }, [
            el('span', { className: 'sidebar-logo-icon', html: storeIcon() }),
            el('span', { className: 'sidebar-logo-text', text: 'Thunder' })
        ]),
        el('div', { className: 'sidebar-nav' },
            navItems.map(item => {
                const btn = el('button', {
                    className: 'sidebar-nav-item',
                    'data-path': item.path,
                    html: `<span class="sidebar-nav-icon">${item.icon}</span><span class="sidebar-nav-label">${item.label}</span>`,
                    onClick: () => navigate(item.path)
                });
                return btn;
            })
        ),
        el('div', { className: 'sidebar-footer' }, [
            el('div', { className: 'sidebar-version', text: 'v0.1.0-nightly' })
        ])
    ]);

    container.appendChild(sidebar);

    function updateActive() {
        const path = getCurrentPath();
        sidebar.querySelectorAll('.sidebar-nav-item').forEach(btn => {
            const itemPath = btn.getAttribute('data-path');
            const isActive = itemPath === '/'
                ? path === '/'
                : path.startsWith(itemPath);
            btn.classList.toggle('active', isActive);
        });
    }

    updateActive();
    window.addEventListener('hashchange', updateActive);
}
