/* Core Application Client and Session Management */

const API = {
    async request(url, options = {}) {
        const token = localStorage.getItem('token');
        const headers = options.headers || {};
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        try {
            const response = await fetch(url, { ...options, headers });
            
            if (response.status === 401 && !url.includes('/auth/login') && !url.includes('/auth/register')) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return null;
            }

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || data.error || 'Request failed');
            }
            return data;
        } catch (err) {
            console.error('API Error:', err);
            throw err;
        }
    },

    getCurrentUser() {
        const u = localStorage.getItem('user');
        return u ? JSON.parse(u) : null;
    },

    async logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        try {
            await fetch('/api/v1/auth/logout', { method: 'POST' });
        } catch (e) {
            console.error('Logout error:', e);
        }
        window.location.href = '/logout';
    }
};

// Global Notifications Toast
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 200);
    }, 4000);
}

// Automatically convert timestamps to browser's exact local timezone
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.local-timestamp').forEach(el => {
        const utcStr = el.getAttribute('data-utc');
        if (utcStr) {
            try {
                const date = new Date(utcStr.endsWith('Z') ? utcStr : utcStr + 'Z');
                if (!isNaN(date.getTime())) {
                    const formatted = date.toLocaleDateString('en-GB', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric'
                    }) + ', ' + date.toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit',
                        hour12: true
                    });
                    el.innerText = formatted;
                }
            } catch (e) {}
        }
    });
});
