/* Authentication & Unified Login/Register Logic */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (tabLogin && tabRegister) {
        tabLogin.addEventListener('click', () => {
            tabLogin.classList.add('active');
            tabRegister.classList.remove('active');
            if (loginForm) loginForm.style.display = 'block';
            if (registerForm) registerForm.style.display = 'none';
        });

        tabRegister.addEventListener('click', () => {
            tabRegister.classList.add('active');
            tabLogin.classList.remove('active');
            if (registerForm) registerForm.style.display = 'block';
            if (loginForm) loginForm.style.display = 'none';
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerText = 'Signing in...';
            }

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
                    }, 400);
                }
            } catch (err) {
                showToast(err.message || 'Invalid credentials', 'error');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerText = 'Sign In';
                }
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerText = 'Creating account...';
            }

            const fullName = document.getElementById('reg-fullname').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const username = document.getElementById('reg-username').value.trim();
            const password = document.getElementById('reg-password').value;

            try {
                await API.request('/api/v1/auth/register', {
                    method: 'POST',
                    body: JSON.stringify({ full_name: fullName, email, username, password })
                });
                
                showToast('Registration successful! Logging you in...', 'success');
                
                // Automatically log in newly registered user
                const loginRes = await API.request('/api/v1/auth/login', {
                    method: 'POST',
                    body: JSON.stringify({ username_or_email: username, password })
                });

                if (loginRes && loginRes.access_token) {
                    localStorage.setItem('token', loginRes.access_token);
                    localStorage.setItem('user', JSON.stringify(loginRes.user));
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 400);
                } else {
                    tabLogin.click();
                    document.getElementById('login-username').value = username;
                }
            } catch (err) {
                showToast(err.message || 'Registration failed', 'error');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerText = 'Create Account';
                }
            }
        });
    }
});
