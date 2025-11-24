// static/js/login.js

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('loginForm');
  
  if (!form) {
    console.error('Login form not found');
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('📋 Форма логіну відправлена');

    const username = document.querySelector('input[name="username"]').value.trim();
    const password = document.querySelector('input[name="password"]').value;

    // Валідація
    if (!username || !password) {
      alert('Please fill in all fields');
      return;
    }

    try {
      console.log('🔄 Надсилаємо запит на сервер...');
      
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });

      console.log('📨 Статус відповіді:', response.status);
      
      const data = await response.json();
      console.log('📥 Дані від сервера:', data);

      if (data.success) {
        console.log('✅ Логін успішний!');
        console.log('🔗 Перенаправляємо на:', data.redirect);
        
        // Затримка для лакомості
        setTimeout(() => {
          window.location.href = data.redirect || '/';
        }, 500);
        
      } else {
        console.error('❌ Помилка логіну:', data.error);
        alert(data.error || 'Login failed');
      }
    } catch (error) {
      console.error('❌ Помилка мережи:', error);
      alert('Network error. Check console.');
    }
  });
});