// Обработчик для кнопки Organizer
document.getElementById('organizer-button').addEventListener('click', () => {
    // Переход на страницу для Organizer
    window.location.href = 'organizer-page.html'; // Замените 'organizer-page.html' на имя вашей следующей страницы
  });
  
  document.getElementById('register-button').addEventListener('click', () => {
    const data = {
        user_type: 'Fan', // Или 'Organizer', в зависимости от кнопки
        login: document.getElementById('login').value,
        password: document.getElementById('password').value,
    };

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => console.error('Error:', error));
});
