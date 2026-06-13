import { el, formatNumber } from '../utils.js';
import { renderEmptyState } from '../components/emptystate.js';
import { navigate } from '../router.js';

const mockInstalled = [
    { id: 'open-interpreter', name: 'Open Interpreter', version: '0.2.0', status: 'installed', lastLaunched: '2025-05-28' },
    { id: 'autogpt', name: 'AutoGPT', version: '0.5.0', status: 'update', lastLaunched: '2025-05-20' }
];

export function renderLibrary(container) {
    container.innerHTML = '';

    const header = el('div', { className: 'view-header' }, [
        el('h1', { className: 'view-title', text: 'Your Library' }),
        el('p', { className: 'view-subtitle', text: 'Manage your installed applications' })
    ]);

    const filterTabs = el('div', { className: 'library-filters' }, [
        createFilterTab('all', 'All', true),
        createFilterTab('updatable', 'Updatable', false),
        createFilterTab('running', 'Running', false)
    ]);

    const listContainer = el('div', { className: 'library-list' });

    container.appendChild(header);
    container.appendChild(filterTabs);
    container.appendChild(listContainer);

    renderLibraryList(listContainer, mockInstalled);
}

function createFilterTab(id, label, active) {
    return el('button', {
        className: `library-filter-tab ${active ? 'active' : ''}`,
        'data-filter': id,
        text: label,
        onClick: (e) => {
            document.querySelectorAll('.library-filter-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
        }
    });
}

function renderLibraryList(container, apps) {
    container.innerHTML = '';

    if (apps.length === 0) {
        renderEmptyState(container, {
            type: 'library',
            title: 'No apps installed',
            description: 'Browse the Store to discover and install apps',
            action: { label: 'Open Store', handler: () => navigate('/store') }
        });
        return;
    }

    const list = el('div', { className: 'library-items' },
        apps.map(app => createLibraryRow(app))
    );

    container.appendChild(list);
}

function createLibraryRow(app) {
    const statusMap = {
        installed: { label: 'Installed', class: 'status-installed' },
        update: { label: 'Update Available', class: 'status-update' },
        running: { label: 'Running', class: 'status-running' }
    };

    const status = statusMap[app.status] || statusMap.installed;

    return el('div', { className: 'library-row' }, [
        el('div', { className: 'library-row-icon', text: app.name.charAt(0).toUpperCase() }),
        el('div', { className: 'library-row-info' }, [
            el('h3', { className: 'library-row-name', text: app.name }),
            el('div', { className: 'library-row-meta' }, [
                el('span', { className: 'library-row-version', text: `v${app.version}` }),
                el('span', { className: `library-row-status ${status.class}`, text: status.label })
            ])
        ]),
        el('div', { className: 'library-row-actions' }, [
            el('button', {
                className: 'btn btn-green btn-sm',
                text: 'Launch',
                onClick: () => console.log('Launch:', app.id)
            }),
            app.status === 'update' ? el('button', {
                className: 'btn btn-secondary btn-sm',
                text: 'Update',
                onClick: () => console.log('Update:', app.id)
            }) : null,
            el('button', {
                className: 'btn btn-danger btn-sm',
                text: 'Uninstall',
                onClick: () => console.log('Uninstall:', app.id)
            })
        ].filter(Boolean))
    ]);
}
