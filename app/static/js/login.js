document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const usernameInput = document.getElementById('username-input');
    const passwordInput = document.getElementById('password-input');
    const showPasswordBtn = document.getElementById('show-password-btn');
    const loginBtn = document.getElementById('login-btn');
    
    // Show/Hide password
    showPasswordBtn.addEventListener('click', function(e) {
        e.preventDefault();
        // знайдемо будь-який текстовий вузол всередині кнопки
        const btnText = this.querySelector('div') || this;
        
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
    
    // Helper: enable/disable button styles
    function setSubmitting(isSubmitting) {
        loginBtn.disabled = isSubmitting;
        loginBtn.style.opacity = isSubmitting ? '0.5' : '1';
    }

    // Form submission (відправляємо JSON)
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        
        if (!username || !password) {
            alert('Введіть ім\'я користувача та пароль.');
            return;
        }
        
        setSubmitting(true);

        const payload = {
            username: username,
            password: password
        };

        try {
            const resp = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Accept': 'application/json'
                    // Якщо є CSRF токен у meta-тегу:
                    // 'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify(payload),
                credentials: 'same-origin'
            });

            // Перевіряємо HTTP-статус
            if (!resp.ok) {
                // якщо сервер повернув JSON з помилкою — виведемо її
                let errText = `HTTP ${resp.status}`;
                try {
                    const errJson = await resp.json();
                    errText = errJson.error || errJson.message || errText;
                } catch (e) {
                    // не JSON — лишимо код помилки
                }
                throw new Error(errText);
            }

            const data = await resp.json();

            if (data.success) {
                // якщо сервер повертає redirect або просто /
                window.location.href = data.redirect || '/';
            } else {
                alert(data.error || 'Невірне ім\'я користувача або пароль');
                setSubmitting(false);
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Помилка входу. Спробуйте ще раз. ' + (error.message ? `(${error.message})` : ''));
            setSubmitting(false);
        }
    });
    
    // Auto-focus on first input
    usernameInput.focus();
});
