// Main JavaScript file for College Bus Tracking System

// Global variables
let currentUser = null;
let notificationPermission = false;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Request notification permission
    requestNotificationPermission();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize real-time updates
    if (window.location.pathname === '/dashboard' || 
        window.location.pathname === '/bus_tracking' ||
        window.location.pathname === '/driver') {
        startRealTimeUpdates();
    }
    
    // Initialize geolocation if needed
    if (navigator.geolocation) {
        console.log('Geolocation is available');
    } else {
        console.warn('Geolocation is not available');
    }
}

// Notification functions
function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(function(permission) {
            notificationPermission = permission === 'granted';
        });
    }
}

function showNotification(title, message) {
    if (notificationPermission) {
        new Notification(title, {
            body: message,
            icon: '/static/favicon.ico'
        });
    }
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Real-time updates
function startRealTimeUpdates() {
    // Update bus locations every 10 seconds
    setInterval(function() {
        updateBusLocations();
    }, 10000);
}

function updateBusLocations() {
    fetch('/api/bus_locations')
        .then(response => response.json())
        .then(buses => {
            // Dispatch custom event with bus data
            const event = new CustomEvent('busLocationsUpdated', { 
                detail: buses 
            });
            document.dispatchEvent(event);
        })
        .catch(error => {
            console.error('Error updating bus locations:', error);
        });
}

// Utility functions
function formatDistance(meters) {
    if (meters < 1000) {
        return Math.round(meters) + 'm';
    } else {
        return (meters / 1000).toFixed(1) + 'km';
    }
}

function formatTime(minutes) {
    if (minutes < 1) {
        return 'Now';
    } else if (minutes === 1) {
        return '1 minute';
    } else {
        return Math.round(minutes) + ' minutes';
    }
}

function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371000; // Earth's radius in meters
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Location functions
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                });
            },
            (error) => {
                reject(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        );
    });
}

// Map utilities
function createCustomIcon(iconClass, color, size = 20) {
    return L.divIcon({
        className: 'custom-marker',
        html: `<i class="${iconClass}" style="color: ${color}; font-size: ${size}px;"></i>`,
        iconSize: [size + 10, size + 10],
        iconAnchor: [(size + 10) / 2, (size + 10) / 2]
    });
}

function addMarkerToMap(map, lat, lng, popupContent, icon) {
    const marker = L.marker([lat, lng], { icon: icon })
        .bindPopup(popupContent)
        .addTo(map);
    return marker;
}

// Error handling
function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    
    // Show user-friendly error message
    showAlert(userMessage, 'error');
    
    // Log error details for debugging
    if (error.message) {
        console.error('Error message:', error.message);
    }
    if (error.stack) {
        console.error('Error stack:', error.stack);
    }
}

// Alert system
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertContainer.style.position = 'fixed';
    alertContainer.style.top = '20px';
    alertContainer.style.right = '20px';
    alertContainer.style.zIndex = '9999';
    alertContainer.style.minWidth = '300px';
    
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-remove alert after duration
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.parentNode.removeChild(alertContainer);
        }
    }, duration);
}

// Local storage utilities
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return defaultValue;
    }
}

// Network status
function checkNetworkStatus() {
    return navigator.onLine;
}

window.addEventListener('online', function() {
    showAlert('Connection restored', 'success', 3000);
});

window.addEventListener('offline', function() {
    showAlert('Connection lost. Some features may not work.', 'warning', 5000);
});

// Form validation
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Loading indicator
function showLoading(element) {
    const loadingHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    if (element) {
        element.innerHTML = loadingHTML;
    }
}

function hideLoading(element, originalContent) {
    if (element && originalContent) {
        element.innerHTML = originalContent;
    }
}

// Mobile detection
function isMobile() {
    return window.innerWidth <= 768;
}

// Responsive map resize
function resizeMap(mapInstance) {
    if (mapInstance) {
        setTimeout(() => {
            mapInstance.invalidateSize();
        }, 100);
    }
}

// Export functions for use in other scripts
window.BusTracker = {
    getCurrentLocation,
    createCustomIcon,
    addMarkerToMap,
    handleError,
    showAlert,
    formatDistance,
    formatTime,
    calculateDistance,
    validateForm,
    showLoading,
    hideLoading,
    isMobile,
    resizeMap
};
