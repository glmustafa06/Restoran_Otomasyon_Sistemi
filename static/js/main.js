/**
 * Ana JavaScript Dosyası
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    initTooltips();

    // Initialize animations
    initAnimations();
});

// Tooltip initialization
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute z-50 px-2 py-1 bg-gray-800 text-white text-xs rounded shadow-lg';
            tooltip.textContent = trigger.dataset.tooltip;
            tooltip.id = 'active-tooltip';
            document.body.appendChild(tooltip);

            const rect = trigger.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
        });

        trigger.addEventListener('mouseleave', () => {
            const tooltip = document.getElementById('active-tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// Scroll animations
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(el => observer.observe(el));
}

// Real-time updates (SSE)
function initRealtimeUpdates(endpoint, callback) {
    if (typeof EventSource !== 'undefined') {
        const eventSource = new EventSource(endpoint);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            callback(data);
        };

        eventSource.onerror = () => {
            console.log('SSE connection error, retrying...');
            eventSource.close();
            setTimeout(() => initRealtimeUpdates(endpoint, callback), 5000);
        };

        return eventSource;
    }
}

// Auto-refresh data
function autoRefresh(callback, interval = 30000) {
    setInterval(callback, interval);
}

// Table status color helper
function getStatusColor(status) {
    const colors = {
        'empty': 'bg-green-500/20 text-green-400',
        'occupied': 'bg-red-500/20 text-red-400',
        'reserved': 'bg-blue-500/20 text-blue-400',
        'cleaning': 'bg-yellow-500/20 text-yellow-400',
        'pending': 'bg-yellow-500/20 text-yellow-400',
        'preparing': 'bg-orange-500/20 text-orange-400',
        'ready': 'bg-green-500/20 text-green-400',
        'served': 'bg-blue-500/20 text-blue-400',
        'paid': 'bg-gray-500/20 text-gray-400'
    };
    return colors[status] || 'bg-gray-500/20 text-gray-400';
}

// Status label helper
function getStatusLabel(status) {
    const labels = {
        'empty': 'Boş',
        'occupied': 'Dolu',
        'reserved': 'Rezerve',
        'cleaning': 'Temizleniyor',
        'pending': 'Bekliyor',
        'preparing': 'Hazırlanıyor',
        'ready': 'Hazır',
        'served': 'Servis Edildi',
        'paid': 'Ödendi'
    };
    return labels[status] || status;
}
