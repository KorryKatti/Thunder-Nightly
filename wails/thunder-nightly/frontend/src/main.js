import './style.css';
import './app.css';
import './components.css';

import { addRoute, initRouter } from './router.js';
import { setState } from './state.js';
import { renderSidebar } from './components/sidebar.js';
import { renderStatusBar } from './components/statusbar.js';
import { renderHome } from './views/home.js';
import { renderAppDetail } from './views/appdetail.js';
import { renderSettings } from './views/settings.js';

function renderApp() {
    const app = document.getElementById('app');
    app.innerHTML = '';

    const body = document.createElement('div');
    body.className = 'app-body';

    const sidebarContainer = document.createElement('div');
    sidebarContainer.className = 'sidebar-container';

    const mainContent = document.createElement('div');
    mainContent.className = 'main-content';
    mainContent.id = 'main-content';

    body.appendChild(sidebarContainer);
    body.appendChild(mainContent);
    app.appendChild(body);

    renderSidebar(sidebarContainer);
    renderStatusBar(app);

    addRoute('/', (params) => {
        setState('currentView', 'home');
        renderHome(mainContent);
    });

    addRoute('/app/:url', (params) => {
        setState('currentView', 'app');
        renderAppDetail(mainContent, params.url);
    });

    addRoute('/settings', (params) => {
        setState('currentView', 'settings');
        renderSettings(mainContent);
    });

    initRouter();
    updateStatusBar();
}

async function updateStatusBar() {
    // Will be populated with real data
}

document.addEventListener('DOMContentLoaded', renderApp);
