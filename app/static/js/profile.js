document.addEventListener('DOMContentLoaded', function() {
    // Follow button functionality
    const followBtn = document.getElementById('follow-btn');
    let isFollowing = false;
    
    followBtn.addEventListener('click', function() {
        const username = '{{ user.username }}';
        
        fetch(`/api/user/${username}/follow`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    isFollowing = !isFollowing;
                    const span = this.querySelector('span');
                    
                    if (isFollowing) {
                        span.textContent = 'Відписатися';
                        this.style.backgroundColor = 'var(--ig-highlight-background)';
                        this.style.color = 'var(--ig-primary-text)';
                    } else {
                        span.textContent = 'Підписатися';
                        this.style.backgroundColor = 'var(--ig-primary-button-background)';
                        this.style.color = '#ffffff';
                    }
                }
            });
    });
    
    // Grid hover effects
    document.querySelectorAll('._aagw').forEach(item => {
        const overlay = item.querySelector('._aagz');
        
        item.addEventListener('mouseenter', function() {
            if (overlay) {
                overlay.style.opacity = '1';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            if (overlay) {
                overlay.style.opacity = '0';
            }
        });
    });
});