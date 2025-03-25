class Auth {
    static async login(email, password) {
        try {
            const response = await fetch(CONFIG.API_URL + CONFIG.AUTH_ENDPOINTS.LOGIN, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password }),
                credentials: 'include'
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }

            localStorage.setItem('user', JSON.stringify(data.user));
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    static async register(userData) {
        try {
            const response = await fetch(CONFIG.API_URL + CONFIG.AUTH_ENDPOINTS.REGISTER, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Registration failed');
            }

            return data;
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    static async verifyEmail(token) {
        try {
            const response = await fetch(CONFIG.API_URL + CONFIG.AUTH_ENDPOINTS.VERIFY_EMAIL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Email verification failed');
            }

            return data;
        } catch (error) {
            console.error('Email verification error:', error);
            throw error;
        }
    }

    static async requestPasswordReset(email) {
        try {
            const response = await fetch(CONFIG.API_URL + CONFIG.AUTH_ENDPOINTS.REQUEST_RESET, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Password reset request failed');
            }

            return data;
        } catch (error) {
            console.error('Password reset request error:', error);
            throw error;
        }
    }

    static async resetPassword(token, newPassword) {
        try {
            const response = await fetch(CONFIG.API_URL + CONFIG.AUTH_ENDPOINTS.RESET_PASSWORD, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token, newPassword })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Password reset failed');
            }

            return data;
        } catch (error) {
            console.error('Password reset error:', error);
            throw error;
        }
    }

    static isLoggedIn() {
        const user = localStorage.getItem('user');
        return !!user;
    }

    static getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }

    static logout() {
        localStorage.removeItem('user');
        window.location.href = '/login';
    }
}

// Initialize auth state
document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userMenu = document.getElementById('userMenu');

    if (Auth.isLoggedIn()) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (registerBtn) registerBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
        if (userMenu) userMenu.style.display = 'block';
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (registerBtn) registerBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'none';
    }
});
