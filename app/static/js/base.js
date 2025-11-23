        
        // Global Instagram-like functionality
        document.addEventListener('DOMContentLoaded', function() {
            // Search functionality
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.addEventListener('focus', function() {
                    this.style.borderColor = 'var(--ig-secondary-text)';
                });
                searchInput.addEventListener('blur', function() {
                    this.style.borderColor = 'var(--ig-separator)';
                });
            }
            
            // Active navigation highlighting
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.x5n08af');
            navLinks.forEach(link => {
                if (link.getAttribute('href') === currentPath || 
                    (currentPath.includes(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
                    link.style.fontWeight = '700';
                }
            });
        });