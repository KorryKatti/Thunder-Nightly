import { el } from '../utils.js';
import { getState } from '../state.js';

export function renderStatusBar(container) {
    const bar = el('div', { className: 'statusbar' }, [
        el('div', { className: 'statusbar-left' }, [
            el('span', { className: 'statusbar-brand', html: '⚡ <strong>Thunder</strong>' }),
            el('span', { className: 'statusbar-sep', text: '·' }),
            el('span', { className: 'statusbar-version', text: 'v0.1.0-nightly' })
        ]),
        el('div', { className: 'statusbar-right' }, [
            el('span', { className: 'statusbar-stat', id: 'status-installed', text: '0 installed' }),
            el('span', { className: 'statusbar-sep', text: '·' }),
            el('span', { className: 'statusbar-stat', id: 'status-updates', text: '0 updates' })
        ])
    ]);

    container.appendChild(bar);
}

export function updateStatusBar(installedCount, updateCount) {
    const installedEl = document.getElementById('status-installed');
    const updatesEl = document.getElementById('status-updates');
    if (installedEl) installedEl.textContent = `${installedCount} installed`;
    if (updatesEl) updatesEl.textContent = `${updateCount} updates`;
}
