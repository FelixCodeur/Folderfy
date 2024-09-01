const ROUTES_REQUIRING_LOGIN = [
    '/mail',
    '/calendar',
    '/dashboard'
]
const token = document.cookie?.split('token=')[1]?.split(';')[0];

function showError(error) {
    console.error(error);

    const message = `${error}\n\nIf you didn't select all permissions during sign up, please ensure you grant all permissions. If this issue persists, please contact us for assistance.`;
    alert(message);
}

async function _fetch(url, options, maxRetries = 0) {
    try {
        const _res = await fetch(url, options);
        const _json = await _res.json();
        if (_res.ok && _json.success) {
            return _json;
        } else {
            if (maxRetries > 0) {
                return _fetch(url, options, maxRetries - 1);
            }
            
            showError(_json.message || 'An error occurred.');
        }
    } catch (error) {
        if (maxRetries > 0) {
            return _fetch(url, options, maxRetries - 1);
        }

        showError(error);
    }
}

function onPageLoad() {
    const route = window.location.pathname;
    if (!token && ROUTES_REQUIRING_LOGIN.includes(route)) {
        window.location.href = '/login';
    }
}

onPageLoad();