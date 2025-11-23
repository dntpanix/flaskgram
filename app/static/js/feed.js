document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const postId = this.dataset.postId;
            const svg = this.querySelector('svg');
            const likesCount = document.querySelector(`[data-post-id="${postId}"] .likes-count`);
            
            fetch(`/api/posts/${postId}/like`, { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        likesCount.textContent = data.likes;
                        // Change to filled heart
                        svg.innerHTML = '<path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 4.959-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 0 1 4.708-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 0 1 3.679-1.938m0-2a6.04 6.04 0 0 0-4.797 2.127 6.052 6.052 0 0 0-4.787-2.127A6.985 6.985 0 0 0 .5 9.122c0 3.61 2.55 5.827 5.015 7.97.283.246.569.494.853.747l1.027.918a44.998 44.998 0 0 0 3.518 3.018 2 2 0 0 0 2.174 0 45.263 45.263 0 0 0 3.626-3.115l.922-.824c.293-.26.59-.519.885-.774 2.334-2.025 4.98-4.32 4.98-7.94a6.985 6.985 0 0 0-6.708-7.218Z" fill="red"/>';
                        svg.setAttribute('fill', '#ed4956');
                    }
                });
        });
    });
    
    // Comment input functionality
    document.querySelectorAll('.comment-input').forEach(textarea => {
        const postBtn = textarea.closest('form').querySelector('.post-comment-btn');
        
        textarea.addEventListener('input', function() {
            // Auto-resize
            this.style.height = '18px';
            this.style.height = Math.min(this.scrollHeight, 80) + 'px';
            
            // Enable/disable post button
            if (this.value.trim().length > 0) {
                postBtn.disabled = false;
                postBtn.classList.add('active');
            } else {
                postBtn.disabled = true;
                postBtn.classList.remove('active');
            }
        });
        
        textarea.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey && this.value.trim()) {
                e.preventDefault();
                const postId = this.dataset.postId;
                
                fetch(`/api/posts/${postId}/comment`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ comment: this.value })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        this.value = '';
                        this.style.height = '18px';
                        postBtn.disabled = true;
                        postBtn.classList.remove('active');
                        
                        // Show success feedback
                        const commentsCount = document.querySelector(`[data-post-id="${postId}"] .view-comments`);
                        if (commentsCount) {
                            const currentCount = parseInt(commentsCount.textContent.match(/\d+/)[0]);
                            commentsCount.innerHTML = `<span class="_aacl _aaco _aacu _aacx _aad7 _aade" dir="auto">Переглянути всі коментарі (${currentCount + 1})</span>`;
                        }
                    }
                });
            }
        });
    });
    
    // Post button click
    document.querySelectorAll('.post-comment-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.disabled) {
                const textarea = this.closest('form').querySelector('.comment-input');
                textarea.dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter' }));
            }
        });
    });
});