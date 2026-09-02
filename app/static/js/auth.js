/* Authentication & Unified Login Logic */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (tabLogin && tabRegister) {
        tabLogin.addEventListener('click', () => {
            tabLogin.classList.add('active');
            tabRegister.classList.remove('active');
            loginForm.style.display = 'block';
            registerForm.style.display = 'none';
        });

        tabRegister.addEventListener('click', () => {
            tabRegister.classList.add('active');
            tabLogin.classList.remove('active');
            registerForm.style.display = 'block';
            loginForm.style.display = 'none';
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const usernameOrEmail = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value;

            try {
                const res = await API.request('/api/v1/auth/login', {
                    method: 'POST',
                    body: JSON.stringify({ username_or_email: usernameOrEmail, password })
                });

                if (res && res.access_token) {
                    localStorage.setItem('token', res.access_token);
                    localStorage.setItem('user', JSON.stringify(res.user));
                    showToast('Login successful! Redirecting...', 'success');
                    
                    setTimeout(() => {
                        if (res.user.role === 'admin') {
                            window.location.href = '/admin/dashboard';
                        } else {
                            window.location.href = '/dashboard';
                        }
                    }, 500);
                }
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fullName = document.getElementById('reg-fullname').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const username = document.getElementById('reg-username').value.trim();
            const password = document.getElementById('reg-password').value;

            try {
                await API.request('/api/v1/auth/register', {
                    method: 'POST',
                    body: JSON.stringify({ full_name: fullName, email, username, password })
                });
                showToast('Registration successful! Please log in.', 'success');
                tabLogin.click();
            } catch (err) {
                showToast(err.message, 'error');
            }
        });
    }
});
