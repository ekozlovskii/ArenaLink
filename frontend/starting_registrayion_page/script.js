console.log('Script loaded'); // Проверка загрузки скрипта

// Обработчик для формы организатора
const organizerForm = document.getElementById('organizer-registration-form');
if (organizerForm) {
  organizerForm.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('Organizer form submitted');

    const fileInput = document.getElementById('documents');
    const formData = new FormData();

    formData.append('login', document.getElementById('login').value);
    formData.append('password', document.getElementById('password').value);
    formData.append('organization', document.getElementById('organization').value);
    formData.append('contact', document.getElementById('contact').value);
    formData.append('documents', fileInput.files[0]);

    console.log('Form data prepared:', formData);

    fetch('http://127.0.0.1:5000/register_organizer', {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(errorData => {
          throw new Error(errorData.error || 'An unexpected error occurred'); // Проверяем сообщение об ошибке
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Response:', data);
      alert('Organizer registration successful!');
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message); // Показываем сообщение об ошибке
    });
  });
} else {
  console.error('Form with ID "organizer-registration-form" not found');
}

// Обработчик для формы фаната
const fanForm = document.getElementById('fan-registration-form');
if (fanForm) {
  fanForm.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('Fan form submitted');

    const data = {
      login: document.getElementById('login').value,
      name: document.getElementById('name').value,
      password: document.getElementById('password').value
    };

    fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(errorData => {
          throw new Error(errorData.error || 'An unexpected error occurred'); // Проверяем сообщение об ошибке
        });
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message);
      alert('Fan registration successful!');
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message); // Показываем сообщение об ошибке
    });
  });
} else {
  console.error('Form with ID "fan-registration-form" not found');
}

// Обработчик для формы входа
const loginForm = document.querySelector('form');
if (loginForm) {
  loginForm.addEventListener('submit', function (event) {
    event.preventDefault();
    console.log('Login form submitted');

    const data = {
      login: document.getElementById('login').value,
      password: document.getElementById('password').value
    };

    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(errorData => {
          throw new Error(errorData.error);
        });
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message);
      alert(`Welcome! Your role: ${data.role}`);
      // Здесь можно добавить логику для перенаправления
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message); // Показываем сообщение об ошибке
    });
  });
} else {
  console.error('Login form not found');
}