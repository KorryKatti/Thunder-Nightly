import {
    CheckUVInstalled,
    GetUVVersion,
    InstallUV,
    GetRepoInfo,
    GetReadme,
    InstallApp,
    OpenExternal
} from '../wailsjs/go/main/App';

export async function checkUV() {
    try {
        const installed = await CheckUVInstalled();
        const version = installed ? await GetUVVersion() : '';
        return { installed, version };
    } catch (e) {
        console.error('CheckUV error:', e);
        return { installed: false, version: '' };
    }
}

export async function installUV() {
    try {
        const output = await InstallUV();
        return { success: true, output };
    } catch (e) {
        console.error('InstallUV error:', e);
        return { success: false, error: String(e) };
    }
}

export async function fetchRepoInfo(url) {
    try {
        console.log('Fetching repo info for:', url);
        const result = await GetRepoInfo(url);
        console.log('Repo info result:', result);
        return result;
    } catch (e) {
        console.error('GetRepoInfo error:', e);
        throw e;
    }
}

export async function fetchReadme(url) {
    try {
        return await GetReadme(url);
    } catch (e) {
        console.error('GetReadme error:', e);
        return '';
    }
}

export async function installApp(url) {
    try {
        const output = await InstallApp(url);
        return { success: true, output };
    } catch (e) {
        console.error('InstallApp error:', e);
        return { success: false, error: String(e) };
    }
}

export async function openExternal(url) {
    try {
        await OpenExternal(url);
    } catch (e) {
        console.error('OpenExternal error:', e);
    }
}
