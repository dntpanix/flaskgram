document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const usernameInput = document.getElementById('username-input');
    const passwordInput = document.getElementById('password-input');
    const showPasswordBtn = document.getElementById('show-password-btn');
    const loginBtn = document.getElementById('login-btn');
    
    // Show/Hide password
    showPasswordBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const btnText = this.querySelector('div');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            btnText.textContent = 'Сховати';
        } else {
            passwordInput.type = 'password';
            btnText.textContent = 'Показати';
        }
    });
    
    // Toggle show password button visibility
    passwordInput.addEventListener('input', function() {
        showPasswordBtn.style.display = this.value.length > 0 ? 'block' : 'none';
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = usernameInput.value;
        const password = passwordInput.value;
        
        if (!username || !password) {
            return;
        }
        
        // Disable button during submission
        loginBtn.disabled = true;
        loginBtn.style.opacity = '0.5';
        
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                alert(data.error || 'Невірне ім\'я користувача або пароль');
                loginBtn.disabled = false;
                loginBtn.style.opacity = '1';
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            alert('Помилка входу. Спробуйте ще раз.');
            loginBtn.disabled = false;
            loginBtn.style.opacity = '1';
        });
    });
    
    // Auto-focus on first input
    usernameInput.focus();
});
