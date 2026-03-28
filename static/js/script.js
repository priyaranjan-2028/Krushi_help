document.addEventListener('DOMContentLoaded', () => {
    const acceptedTermsKey = 'krushi_terms_accepted';

    /* =======================================
       Terms Routing
       ======================================= */
    const body = document.body;
    if (body.classList.contains('index-page') && !localStorage.getItem(acceptedTermsKey)) {
        window.location.href = body.dataset.termsUrl;
        return;
    }

    if (body.classList.contains('terms-page')) {
        const acceptTermsPageBtn = document.getElementById('accept-terms-page-btn');
        const closeTermsPageBtn = document.getElementById('close-terms-page-btn');
        if (acceptTermsPageBtn) {
            acceptTermsPageBtn.addEventListener('click', () => {
                localStorage.setItem(acceptedTermsKey, 'true');
                window.location.href = body.dataset.indexUrl;
            });
        }
        if (closeTermsPageBtn) {
            closeTermsPageBtn.addEventListener('click', () => {
                window.location.href = body.dataset.indexUrl;
            });
        }
        return;
    }

    /* =======================================
       Sticky Navbar & Scroll Effects
       ======================================= */
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    /* =======================================
       Mobile Menu Toggle
       ======================================= */
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const navActions = document.querySelector('.nav-actions');

    mobileToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        if(navLinks.classList.contains('active')) {
            // Quick hack to show buttons in mobile menu if needed
            navLinks.style.display = 'flex';
        } else {
             navLinks.style.display = 'none';
             setTimeout(() => navLinks.style.display = '', 200); // reset after transition
        }
    });

    /* =======================================
       Smooth Scrolling for Anchor Links
       ======================================= */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Adjust scroll position for fixed header
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
  
                window.scrollTo({
                     top: offsetPosition,
                     behavior: "smooth"
                });

                // Close mobile menu if open
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('active');
                    navLinks.style.display = '';
                }
            }
        });
    });

    /* =======================================
       Buy Now Button Interaction (Toast)
       ======================================= */
    const buyButtons = document.querySelectorAll('.buy-btn');
    const toastContainer = document.getElementById('toast-container');

    const showToast = (message) => {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <span class="icon">✅</span>
            <div>
                <strong>Success</strong><br>
                <span>${message}</span>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Trigger reflow to apply transition
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 400); // Wait for fade out animation
        }, 3000);
    };

    buyButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const productCard = e.target.closest('.product-card');
            const productTitle = productCard.querySelector('.product-title').innerText;
            
            // Disable button temporarily to prevent spam clicks
            const originalText = e.target.innerText;
            e.target.innerText = "Adding...";
            e.target.style.opacity = '0.7';
            e.target.disabled = true;

            setTimeout(() => {
                showToast(`Added <strong>${productTitle}</strong> to your cart!`);
                e.target.innerText = "Buy Again";
                e.target.style.opacity = '1';
                e.target.disabled = false;
            }, 600);
        });
    });

    /* =======================================
       Login Button Click
       ======================================= */
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            alert('Aadhaar Login portal simulation initializing...');
        });
    }

    /* =======================================
       Hero Fade In Animation Trigger
       ======================================= */
    // Ensure fade-in elements are visible even if JS fails, but we apply classes in HTML
    // and rely on native CSS animations which trigger on page load via class.
});
