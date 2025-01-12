document.getElementById('fan-registration-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Предотвращает перезагрузку страницы

  const data = {
      login: document.getElementById('login').value,
      name: document.getElementById('name').value,
      password: document.getElementById('password').value
  };

  fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json', // Указываем формат данных
      },
      body: JSON.stringify(data), // Преобразуем объект в JSON
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      console.log(data.message);
      alert('Registration successful!');
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Registration failed. Please try again.');
  });
});
