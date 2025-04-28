console.log('Script loaded'); // Проверка загрузки скрипта

// -------------------- РЕГИСТРАЦИЯ ОРГАНИЗАТОРА --------------------
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

    fetch('http://127.0.0.1:5000/register_organizer', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      alert('Organizer registration successful!');
      window.location.href = 'login.html';
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
}

// -------------------- РЕГИСТРАЦИЯ ФАНАТА --------------------
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
    .then(response => response.json())
    .then(data => {
      alert('Fan registration successful!');
      window.location.href = 'login.html';
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
}

// -------------------- АВТОРИЗАЦИЯ --------------------
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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
      sessionStorage.setItem('userName', data.name);
      sessionStorage.setItem('userRole', data.role);
      sessionStorage.setItem('user_id', data.user_id); // ✅ Теперь ID пользователя сохраняется!

      console.log('Logged in as:', sessionStorage.getItem('userId'));  // Проверка в консоли

      window.location.href = 'main.html'; // Перенаправление на главную страницу
    })
    .catch(error => {
      console.error('Error:', error);
      alert(error.message);
    });
  });
}

// -------------------- ДОБАВЛЕНИЕ МАТЧА (ОРГАНИЗАТОР) --------------------
const matchForm = document.getElementById('add-match-form');
if (matchForm) {
  matchForm.addEventListener('submit', function(event) {
    event.preventDefault();
    console.log('Match form submitted');

    const formData = new FormData(matchForm);

    // ✅ Проверяем, есть ли user_id в sessionStorage
    const userId = sessionStorage.getItem('user_id');
    if (!userId) {
      alert('Error: You are not logged in as an organizer.');
      return;
    }
    formData.append('created_by', userId);

    fetch('http://127.0.0.1:5000/add_match', {
      method: 'POST',
      body: formData,
      credentials: 'include'  // ✅ Теперь cookies сессии будут передаваться
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert('Failed to add match. ' + data.error);
      } else {
        alert('Match added successfully!');
        window.location.href = 'organizer-dashboard.html';
      }
    })
    .catch(error => {
      console.error('Error adding match:', error);
      alert('Failed to add match. Please try again.');
    });
  });
}


// -------------------- ЗАГРУЗКА СПИСКА МАТЧЕЙ НА ГЛАВНОЙ --------------------
document.addEventListener('DOMContentLoaded', function () {
  const matchesList = document.getElementById('matches-list');
  if (matchesList) {
    fetch('http://127.0.0.1:5000/matches')
      .then(response => response.json())
      .then(matches => {
        if (matches.length === 0) {
          matchesList.innerHTML = '<p>No matches available</p>';
          return;
        }
        matches.forEach(match => {
          const div = document.createElement('div');
          div.classList.add('match-item');
          div.innerHTML = `<strong>${match.name}</strong> - ${match.date} at ${match.stadium}`;
          matchesList.appendChild(div);
        });
      })
      .catch(error => console.error('Error loading matches:', error));
  }
});

// -------------------- ПЕРЕХОД В ЛИЧНЫЙ КАБИНЕТ --------------------
document.addEventListener('DOMContentLoaded', function () {
  const dashboardButton = document.getElementById('dashboard-button');
  if (dashboardButton) {
    const userRole = sessionStorage.getItem('userRole');

    if (userRole === 'fan') {
      dashboardButton.onclick = function () {
        window.location.href = 'fan-dashboard.html';
      };
    } else if (userRole === 'organizer') {
      dashboardButton.onclick = function () {
        window.location.href = 'organizer-dashboard.html';
      };
    } else {
      dashboardButton.disabled = true;
      dashboardButton.innerText = 'Please log in';
    }
  }
});

// -------------------- ОЧИСТКА СЕССИИ (ВЫХОД) --------------------
const logoutButton = document.getElementById('logout-button');
if (logoutButton) {
  logoutButton.addEventListener('click', () => {
    sessionStorage.clear();
    window.location.href = 'login.html';
  });
}
