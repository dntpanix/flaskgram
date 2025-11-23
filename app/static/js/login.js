// login.js - правильне надсилання JSON з Content-Type заголовком

const form = document.getElementById('loginForm');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.querySelector('input[name="username"]').value;
  const password = document.querySelector('input[name="password"]').value;

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  // ✅ ЦЕ КРИТИЧНО!
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const data = await response.json();

    if (data.success) {
      // Успішний логін
      window.location.href = data.redirect || '/';
    } else {
      // Помилка логіну
      alert(data.error || 'Помилка під час логіну');
    }
  } catch (error) {
    console.error('Помилка:', error);
    alert('Помилка при надсиланні запиту');
  }
});