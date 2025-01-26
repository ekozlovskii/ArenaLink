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
          throw new Error(errorData.error || 'An unexpected error occurred');
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Organizer registration successful:', data);
      alert('Organizer registration successful!');
      window.location.href = 'login.html';
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(errorData => {
          throw new Error(errorData.error || 'An unexpected error occurred');
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Fan registration successful:', data);
      alert('Fan registration successful!');
      window.location.href = 'login.html';
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
}

// Обработчик для формы входа
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('Login form submitted');

    const data = {
      login: document.getElementById('login').value.trim(),
      password: document.getElementById('password').value.trim()
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
          throw new Error(errorData.error || 'Invalid credentials');
        });
      }
      return response.json();
    })
    .then(data => {
      console.log('Login successful:', data);
      sessionStorage.setItem('userName', data.name);
      sessionStorage.setItem('userRole', data.role);

      // Перенаправление в зависимости от роли пользователя
      if (data.role === 'organizer') {
        window.location.href = 'organizer-dashboard.html';
      } else if (data.role === 'fan') {
        window.location.href = 'fan-dashboard.html';
      } else {
        alert('Unknown role. Please contact support.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
}


// Проверка сессии пользователя при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
  const fanName = sessionStorage.getItem('fanName');
  if (fanName) {
    const nameField = document.getElementById('fan-name-display');
    if (nameField) {
      nameField.textContent = fanName;
    }
  }

  const matchesList = document.getElementById('matches-list');
  if (matchesList) {
    fetch('http://127.0.0.1:5000/my_matches')
      .then(response => response.json())
      .then(data => {
        if (data.length === 0) {
          matchesList.innerHTML = '<p>No matches found.</p>';
          return;
        }

        data.forEach(match => {
          const matchItem = document.createElement('div');
          matchItem.classList.add('match-item');
          matchItem.innerHTML = `
            <div class="match-date">${match.date_time}</div>
            <div class="match-details">
              <strong>${match.match_name}</strong> - ${match.stadium_name}
              <br>Tickets: ${match.ticket_quantity} | Price: ₽${match.ticket_price}
            </div>
          `;
          matchItem.addEventListener('click', () => {
            window.location.href = `edit-match.html?id=${match.id}`;
          });
          matchesList.appendChild(matchItem);
        });
      })
      .catch(error => {
        console.error('Error loading matches:', error);
        matchesList.innerHTML = '<p>Error loading matches. Please try again later.</p>';
      });
  }
});

// Функция добавления матча
function addMatch() {
  window.location.href = 'add-match.html';
}

// Очистка сессии при выходе
const logoutButton = document.getElementById('logout-button');
if (logoutButton) {
  logoutButton.addEventListener('click', () => {
    sessionStorage.clear();
    window.location.href = 'login.html';
  });
}
