/**
 * Animações JavaScript para Dashboard Premium
 * Inclui: counter animations, sidebar toggle, chart transitions
 */

// ============================================================
// Counter Animation
// ============================================================

function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    const isDecimal = target % 1 !== 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        if (isDecimal) {
            element.textContent = current.toLocaleString('pt-BR', {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            });
        } else {
            element.textContent = Math.floor(current).toLocaleString('pt-BR');
        }
    }, 16);
}

// Initialize counter animations
function initCounterAnimations() {
    const metricValues = document.querySelectorAll('[data-testid="stMetricValue"]');
    metricValues.forEach(el => {
        const text = el.textContent.trim();
        // Extract numeric value
        const numericMatch = text.match(/[\d,.]+/);
        if (numericMatch) {
            const target = parseFloat(numericMatch[0].replace(/\./g, '').replace(',', '.'));
            if (!isNaN(target)) {
                // Store original for re-animation
                el.dataset.targetValue = target;
                el.dataset.isDecimal = (target % 1 !== 0).toString();
                animateCounter(el, target);
            }
        }
    });
}

// ============================================================
// Sidebar Toggle
// ============================================================

function initSidebarToggle() {
    // Create toggle button if not exists
    if (!document.getElementById('sidebar-toggle-btn')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'sidebar-toggle-btn';
        toggleBtn.setAttribute('aria-label', 'Alternar sidebar');
        toggleBtn.innerHTML = '☰';
        toggleBtn.style.cssText = `
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1000;
            background: var(--primary, #C46A2B);
            color: white;
            border: none;
            border-radius: 8px;
            width: 44px;
            height: 44px;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        toggleBtn.addEventListener('click', toggleSidebar);
        toggleBtn.addEventListener('mouseenter', () => {
            toggleBtn.style.transform = 'scale(1.05)';
            toggleBtn.style.boxShadow = '0 6px 16px rgba(0,0,0,0.2)';
        });
        toggleBtn.addEventListener('mouseleave', () => {
            toggleBtn.style.transform = 'scale(1)';
            toggleBtn.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        });
        
        document.body.appendChild(toggleBtn);
    }
    
    // Apply initial state
    applySidebarState();
}

function toggleSidebar() {
    const collapsed = document.body.classList.toggle('sidebar-collapsed');
    localStorage.setItem('sidebar_collapsed', collapsed);
    applySidebarState();
}

function applySidebarState() {
    const collapsed = document.body.classList.contains('sidebar-collapsed');
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    
    if (sidebar) {
        sidebar.style.width = collapsed ? '64px' : '280px';
        sidebar.style.transition = 'width 300ms cubic-bezier(0.4, 0, 0.2, 1)';
    }
    
    if (toggleBtn) {
        toggleBtn.innerHTML = collapsed ? '☰' : '✕';
        toggleBtn.setAttribute('aria-label', collapsed ? 'Expandir sidebar' : 'Recolher sidebar');
    }
    
    // Toggle content visibility
    const sidebarContent = sidebar?.querySelector('.sidebar-content');
    if (sidebarContent) {
        sidebarContent.style.opacity = collapsed ? '0' : '1';
        sidebarContent.style.transition = 'opacity 200ms ease';
        sidebarContent.style.display = collapsed ? 'none' : 'block';
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initCounterAnimations();
    initSidebarToggle();
    
    // Re-apply on Streamlit reruns
    const observer = new MutationObserver(() => {
        initCounterAnimations();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class']
    });
});

// Re-initialize on Streamlit message events (for re-renders)
window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'streamlit:render') {
        setTimeout(() => {
            initCounterAnimations();
            applySidebarState();
        }, 100);
    }
});

// ============================================================
// Chart Animation Helpers
// ============================================================

function animateChartUpdate(chartDiv, newData) {
    if (!chartDiv || !window.Plotly) return;
    
    try {
        Plotly.animate(chartDiv, newData, {
            transition: {
                duration: 500,
                easing: 'cubic-in-out'
            },
            frame: {
                duration: 500,
                redraw: false
            }
        });
    } catch (e) {
        console.warn('Chart animation failed:', e);
    }
}

// ============================================================
// Loading State
// ============================================================

function showLoading(element) {
    element.style.opacity = '0.5';
    element.style.pointerEvents = 'none';
    element.style.position = 'relative';
    
    if (!element.querySelector('.loading-overlay')) {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.style.cssText = `
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255,255,255,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: inherit;
            z-index: 10;
        `;
        overlay.innerHTML = `
            <div style="
                width: 40px; height: 40px;
                border: 3px solid var(--border, #D0DAD4);
                border-top-color: var(--primary, #C46A2B);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <style>
                @keyframes spin { to { transform: rotate(360deg); } }
            </style>
        `;
        element.appendChild(overlay);
    }
}

function hideLoading(element) {
    element.style.opacity = '1';
    element.style.pointerEvents = 'auto';
    const overlay = element.querySelector('.loading-overlay');
    if (overlay) overlay.remove();
}

// Export for use in Streamlit components
window.DashboardAnimations = {
    animateCounter,
    initCounterAnimations,
    toggleSidebar,
    applySidebarState,
    animateChartUpdate,
    showLoading,
    hideLoading
};