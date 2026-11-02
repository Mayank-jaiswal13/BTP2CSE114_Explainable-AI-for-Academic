// ═══════════════════════════════════════════════════════════════
// ACADEMIC RISK PREDICTOR - MAIN JAVASCRIPT
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth transitions
    addSmoothTransitions();
    
    // Form validation
    initializeFormValidation();
}

// ═══════════════════════════════════════════════════════════════
// TOOLTIPS INITIALIZATION
// ═══════════════════════════════════════════════════════════════

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ═══════════════════════════════════════════════════════════════
// SMOOTH TRANSITIONS
// ═══════════════════════════════════════════════════════════════

function addSmoothTransitions() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// ═══════════════════════════════════════════════════════════════
// FORM VALIDATION
// ═══════════════════════════════════════════════════════════════

function initializeFormValidation() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity() === false) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    }
}

// ═══════════════════════════════════════════════════════════════
// NAVBAR ACTIVE STATE
// ═══════════════════════════════════════════════════════════════

function setActiveNavItem() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// LOGOUT FUNCTIONALITY
// ═══════════════════════════════════════════════════════════════

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/logout';
    }
}

// ═══════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getIconClass(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Insert at top of main content
    const mainContent = document.querySelector('.main-content') || document.body;
    mainContent.insertAdjacentHTML('afterbegin', alertHTML);
}

function getIconClass(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// ═══════════════════════════════════════════════════════════════
// RESPONSIVE MENU
// ═══════════════════════════════════════════════════════════════

function toggleMenu() {
    const navbar = document.querySelector('.navbar-collapse');
    if (navbar) {
        navbar.classList.toggle('show');
    }
}

// ═══════════════════════════════════════════════════════════════
// FORM SUBMISSION WITH LOADING STATE
// ═══════════════════════════════════════════════════════════════

function submitFormWithLoading(formId, submitButtonId) {
    const form = document.getElementById(formId);
    const submitBtn = document.getElementById(submitButtonId);
    
    if (form && submitBtn) {
        form.addEventListener('submit', function(e) {
            submitBtn.disabled = true;
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            
            // Restore after submission
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 3000);
        });
    }
}

// ═══════════════════════════════════════════════════════════════
// INITIALIZE ON PAGE LOAD
// ═══════════════════════════════════════════════════════════════

setActiveNavItem();
