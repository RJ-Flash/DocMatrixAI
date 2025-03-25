// Main JavaScript file for ContractAI website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.md\\:hidden');
    if (mobileMenuButton) {
        // Create mobile menu elements if they don't exist in the HTML
        if (!document.querySelector('.mobile-menu')) {
            // Create mobile menu overlay
            const overlay = document.createElement('div');
            overlay.className = 'mobile-menu-overlay';
            document.body.appendChild(overlay);

            // Create mobile menu
            const mobileMenu = document.createElement('div');
            mobileMenu.className = 'mobile-menu';
            mobileMenu.innerHTML = `
                <div class="flex justify-between items-center mb-8">
                    <a href="#" class="text-2xl font-bold text-indigo-600">Contract<span class="text-purple-600">AI</span></a>
                    <button class="close-menu text-gray-500 focus:outline-none">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav class="flex flex-col space-y-4">
                    <a href="#features" class="text-gray-600 hover:text-indigo-600 transition py-2 text-lg">Features</a>
                    <a href="#how-it-works" class="text-gray-600 hover:text-indigo-600 transition py-2 text-lg">How It Works</a>
                    <a href="#pricing" class="text-gray-600 hover:text-indigo-600 transition py-2 text-lg">Pricing</a>
                    <a href="#" class="text-indigo-600 font-medium hover:text-indigo-700 transition py-2 text-lg">Log In</a>
                    <a href="#" class="bg-indigo-600 text-white px-5 py-3 rounded-md hover:bg-indigo-700 transition shadow-sm text-center mt-4">Request Demo</a>
                </nav>
            `;
            document.body.appendChild(mobileMenu);

            // Add click event to close menu button
            document.querySelector('.close-menu').addEventListener('click', function() {
                overlay.classList.remove('open');
                mobileMenu.classList.remove('open');
                document.body.style.overflow = 'auto';
            });

            // Close menu when clicking on overlay
            overlay.addEventListener('click', function() {
                overlay.classList.remove('open');
                mobileMenu.classList.remove('open');
                document.body.style.overflow = 'auto';
            });

            // Close menu when clicking on menu links
            mobileMenu.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function() {
                    overlay.classList.remove('open');
                    mobileMenu.classList.remove('open');
                    document.body.style.overflow = 'auto';
                });
            });
        }

        // Toggle mobile menu
        const overlay = document.querySelector('.mobile-menu-overlay');
        const mobileMenu = document.querySelector('.mobile-menu');
        
        mobileMenuButton.addEventListener('click', function() {
            overlay.classList.add('open');
            mobileMenu.classList.add('open');
            document.body.style.overflow = 'hidden';
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.getAttribute('href') !== "#") {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 80, // Adjust for header height
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // ROI Calculator functionality
    const contractsSlider = document.getElementById('contracts');
    const hoursSlider = document.getElementById('hours');
    const rateSlider = document.getElementById('rate');

    if (contractsSlider && hoursSlider && rateSlider) {
        const contractsValue = document.getElementById('contracts-value');
        const hoursValue = document.getElementById('hours-value');
        const rateValue = document.getElementById('rate-value');
        const currentCost = document.getElementById('current-cost');
        const newCost = document.getElementById('new-cost');
        const savings = document.getElementById('savings');

        function updateCalculator() {
            const contracts = parseInt(contractsSlider.value);
            const hours = parseInt(hoursSlider.value);
            const rate = parseInt(rateSlider.value);

            // Update display values
            contractsValue.textContent = `${contracts} contracts`;
            hoursValue.textContent = `${hours} hours`;
            rateValue.textContent = `$${rate}/hour`;

            // Calculate costs
            const currentCostValue = contracts * hours * rate;
            const newCostValue = currentCostValue * 0.2; // Assuming 80% savings
            const savingsValue = currentCostValue - newCostValue;

            // Update results
            currentCost.textContent = `$${currentCostValue.toLocaleString()}`;
            newCost.textContent = `$${newCostValue.toLocaleString()}`;
            savings.textContent = `$${savingsValue.toLocaleString()}`;
        }

        // Initial calculation
        updateCalculator();

        // Update on slider change
        contractsSlider.addEventListener('input', updateCalculator);
        hoursSlider.addEventListener('input', updateCalculator);
        rateSlider.addEventListener('input', updateCalculator);
    }

    // Form validation for lead capture
    const leadForm = document.querySelector('#request-access form');
    if (leadForm) {
        leadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const firstName = document.getElementById('first-name').value;
            const lastName = document.getElementById('last-name').value;
            const company = document.getElementById('company').value;
            const role = document.getElementById('role').value;
            
            let isValid = true;
            
            // Simple validation
            if (!email || !email.includes('@') || !email.includes('.')) {
                highlightError('email');
                isValid = false;
            }
            
            if (!firstName) {
                highlightError('first-name');
                isValid = false;
            }
            
            if (!lastName) {
                highlightError('last-name');
                isValid = false;
            }
            
            if (!company) {
                highlightError('company');
                isValid = false;
            }
            
            if (!role) {
                highlightError('role');
                isValid = false;
            }
            
            if (isValid) {
                // In a real implementation, this would send data to a server
                // For this demo, we'll show a success message
                leadForm.innerHTML = `
                    <div class="text-center py-8">
                        <svg class="w-16 h-16 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <h3 class="text-2xl font-bold text-gray-800 mb-2">Thank You!</h3>
                        <p class="text-gray-600 mb-6">Your request has been submitted successfully. We'll be in touch soon.</p>
                        <a href="#" class="inline-block bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition">Back to Home</a>
                    </div>
                `;
            }
        });
        
        function highlightError(fieldId) {
            const field = document.getElementById(fieldId);
            field.classList.add('border-red-500');
            field.classList.add('bg-red-50');
            
            field.addEventListener('input', function() {
                field.classList.remove('border-red-500');
                field.classList.remove('bg-red-50');
            }, { once: true });
        }
    }

    // Add animation to elements when they become visible
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .testimonial-card, h2, .bg-indigo-600');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animate-fadeIn');
            }
        });
    };
    
    // Run once on load
    animateOnScroll();
    
    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);

    // FAQ functionality (if present on the page)
    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const answer = question.nextElementSibling;
                answer.classList.toggle('open');
                
                // Toggle plus/minus icon if it exists
                const icon = question.querySelector('svg');
                if (icon) {
                    const isOpen = answer.classList.contains('open');
                    icon.innerHTML = isOpen ? 
                        `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>` :
                        `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>`;
                }
            });
        });
    }
});