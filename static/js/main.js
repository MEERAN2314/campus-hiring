// Main JavaScript for Campus Hiring Platform

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    initScrollEffects();
});

// Initialize scroll effects
function initScrollEffects() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    const navAuth = document.getElementById('navAuth');
    const navUser = document.getElementById('navUser');
    const dashboardLink = document.getElementById('dashboardLink');
    const jobsLink = document.getElementById('jobsLink');
    
    if (token && user) {
        const userData = JSON.parse(user);
        console.log('User data:', userData); // Debug log
        console.log('User type:', userData.user_type); // Debug log
        
        // Show user menu
        if (navAuth) navAuth.style.display = 'none';
        if (navUser) {
            navUser.style.display = 'flex';
            document.getElementById('userName').textContent = userData.full_name;
        }
        if (dashboardLink) dashboardLink.style.display = 'block';
        
        // Set Jobs link based on user type
        if (jobsLink) {
            if (userData.user_type === 'recruiter') {
                console.log('Setting jobs link to /recruiter/jobs'); // Debug log
                jobsLink.href = '/recruiter/jobs';
            } else {
                console.log('Setting jobs link to /jobs'); // Debug log
                jobsLink.href = '/jobs';
            }
        }
        
    } else {
        // Show auth buttons
        if (navAuth) navAuth.style.display = 'flex';
        if (navUser) navUser.style.display = 'none';
        if (dashboardLink) dashboardLink.style.display = 'none';
        if (jobsLink) jobsLink.href = '/jobs';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

// Toggle mobile menu
function toggleMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

// API helper function
async function apiRequest(url, options = {}) {
    const token = localStorage.getItem('token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        // Handle unauthorized
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format time
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Protect routes
function protectRoute(allowedUserTypes = []) {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        window.location.href = '/login';
        return false;
    }
    
    if (allowedUserTypes.length > 0) {
        const userData = JSON.parse(user);
        if (!allowedUserTypes.includes(userData.user_type)) {
            window.location.href = '/';
            return false;
        }
    }
    
    return true;
}

// Export functions for use in other scripts
window.apiRequest = apiRequest;
window.formatDate = formatDate;
window.formatTime = formatTime;
window.showNotification = showNotification;
window.protectRoute = protectRoute;
window.logout = logout;
window.toggleMenu = toggleMenu;
