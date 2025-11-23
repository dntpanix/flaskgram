// static/js/signup.js

const form = document.getElementById('signupForm');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.querySelector('input[name="email"]').value;
  const username = document.querySelector('input[name="username"]').value;
  const password = document.querySelector('input[name="password"]').value;
  const password_confirm = document.querySelector('input[name="password_confirm"]').value;

  // Приховуємо повідомлення про помилку
  errorMessage.style.display = 'none';
  errorMessage.textContent = '';

  try {
    const response = await fetch('/accounts/emailsignup/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  // ✅ ВАЖЛИВО!
      },
      body: JSON.stringify({
        email: email,
        username: username,
        password: password,
        password_confirm: password_confirm
      })
    });

    const data = await response.json();

    if (data.success) {
      // Успішна реєстрація
      alert(data.message);
      window.location.href = data.redirect || '/login';
    } else {
      // Показуємо помилку
      errorMessage.textContent = data.error || 'Помилка реєстрації';
      errorMessage.style.display = 'block';
    }
  } catch (error) {
    console.error('Помилка:', error);
    errorMessage.textContent = 'Помилка при надсиланні запиту';
    errorMessage.style.display = 'block';
  }
});