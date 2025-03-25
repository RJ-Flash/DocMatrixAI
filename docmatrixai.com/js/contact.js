class ContactForm {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (!this.form) return;

        this.submitButton = this.form.querySelector('button[type="submit"]');
        this.setupForm();
    }

    setupForm() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!this.validateForm()) {
                return;
            }

            this.setLoading(true);

            const formData = new FormData(this.form);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                company: formData.get('company'),
                message: formData.get('message')
            };

            try {
                const response = await fetch(CONFIG.API_URL + CONFIG.CONTACT_ENDPOINT, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (!response.ok) {
                    throw new Error(result.message || 'Failed to send message');
                }

                this.showSuccess('Thank you! We will get back to you soon.');
                this.form.reset();
            } catch (error) {
                this.showError(error.message || 'An error occurred. Please try again.');
            } finally {
                this.setLoading(false);
            }
        });
    }

    validateForm() {
        const name = this.form.querySelector('[name="name"]').value.trim();
        const email = this.form.querySelector('[name="email"]').value.trim();
        const message = this.form.querySelector('[name="message"]').value.trim();

        if (!name || !email || !message) {
            this.showError('Please fill in all required fields.');
            return false;
        }

        if (!this.isValidEmail(email)) {
            this.showError('Please enter a valid email address.');
            return false;
        }

        return true;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    setLoading(isLoading) {
        this.submitButton.disabled = isLoading;
        this.submitButton.innerHTML = isLoading ? 
            '<span class="spinner"></span> Sending...' : 
            'Send Message';
    }

    showSuccess(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success';
        alert.innerHTML = message;
        this.form.insertBefore(alert, this.form.firstChild);
        setTimeout(() => alert.remove(), 5000);
    }

    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger';
        alert.innerHTML = message;
        this.form.insertBefore(alert, this.form.firstChild);
        setTimeout(() => alert.remove(), 5000);
    }
}

// Initialize contact form
document.addEventListener('DOMContentLoaded', () => {
    new ContactForm('contactForm');
});
