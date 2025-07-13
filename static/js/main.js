// Main JavaScript file for Disaster Management System
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Real-time clock for emergency dashboard
    updateClock();
    setInterval(updateClock, 1000);

    // Initialize emergency notification system
    initializeEmergencyNotifications();

    // Form validation enhancements
    initializeFormValidation();

    // Search functionality
    initializeSearch();

    // Chart animations
    initializeChartAnimations();
});

// Real-time clock function
function updateClock() {
    const clockElement = document.getElementById('emergency-clock');
    if (clockElement) {
        const now = new Date();
        const timeString = now.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });
        clockElement.textContent = timeString;
    }
}

// Emergency notification system
function initializeEmergencyNotifications() {
    // Check for emergency alerts every 30 seconds
    setInterval(checkEmergencyAlerts, 30000);

    // Check for browser notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

// Check for emergency alerts
function checkEmergencyAlerts() {
    // This would typically fetch from an API
    fetch('/api/disaster-stats')
        .then(response => response.json())
        .then(data => {
            if (data.active_disasters > 0) {
                showEmergencyNotification(data.active_disasters);
            }
        })
        .catch(error => console.log('Error checking alerts:', error));
}

// Show emergency notification
function showEmergencyNotification(activeDisasters) {
    if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification('Emergency Alert', {
            body: `${activeDisasters} active disasters requiring attention`,
            icon: '/static/img/emergency-icon.png',
            badge: '/static/img/emergency-badge.png',
            tag: 'emergency-alert'
        });

        notification.onclick = function() {
            window.focus();
            notification.close();
        };

        setTimeout(() => notification.close(), 10000);
    }
}

// Enhanced form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showFormErrors(form);
            } else {
                showLoadingState(form);
            }
            form.classList.add('was-validated');
        });
    });
}

// Show form errors
function showFormErrors(form) {
    const invalidFields = form.querySelectorAll(':invalid');
    invalidFields.forEach(function(field) {
        const errorMessage = field.validationMessage;
        showFieldError(field, errorMessage);
    });
}

// Show field-specific error
function showFieldError(field, message) {
    let errorElement = field.parentNode.querySelector('.invalid-feedback');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        field.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = message;
    field.classList.add('is-invalid');
}

// Show loading state
function showLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            debounce(performSearch, 300)(searchTerm);
        });
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Perform search
function performSearch(searchTerm) {
    const searchableElements = document.querySelectorAll('[data-searchable]');
    searchableElements.forEach(function(element) {
        const text = element.textContent.toLowerCase();
        if (text.includes(searchTerm) || searchTerm === '') {
            element.style.display = '';
        } else {
            element.style.display = 'none';
        }
    });
}

// Chart animations
function initializeChartAnimations() {
    // Animate charts when they come into view
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const chart = entry.target;
                chart.classList.add('animate-chart');
            }
        });
    });

    const charts = document.querySelectorAll('canvas');
    charts.forEach(function(chart) {
        observer.observe(chart);
    });
}

// Utility functions
const Utils = {
    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container') || createToastContainer();
        const toast = createToast(message, type);
        toastContainer.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    },

    // Validate email format
    validateEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Safe HTML sanitization
    sanitizeHTML: function(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
};

// Create toast container
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Create toast element
function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    const iconClass = {
        'success': 'fas fa-check-circle text-success',
        'error': 'fas fa-exclamation-circle text-danger',
        'warning': 'fas fa-exclamation-triangle text-warning',
        'info': 'fas fa-info-circle text-info'
    }[type];

    toast.innerHTML = `
        <div class="toast-header">
            <i class="${iconClass} me-2"></i>
            <strong class="me-auto">System Alert</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${Utils.sanitizeHTML(message)}
        </div>
    `;

    return toast;
}

// Emergency contact quick dial
function quickDial(number) {
    if (confirm(`Call ${number}?`)) {
        window.location.href = `tel:${number}`;
    }
}

// Export utility functions for use in other scripts
window.DisasterUtils = Utils;
window.quickDial = quickDial;

// PWA service worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Handle offline status
window.addEventListener('online', function() {
    Utils.showToast('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    Utils.showToast('You are offline. Some features may be limited.', 'warning');
});