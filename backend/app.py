import os
from flask import Flask, request, jsonify, Response, make_response, session
from flask_cors import CORS
from models import db, User, Match, Ticket
from datetime import datetime,  timedelta, UTC
import jwt
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Загружаем переменные окружения из .env файла
load_dotenv()

# Проверяем наличие ключей в переменных окружения
if not os.getenv('FLASK_SECRET_KEY') or not os.getenv('JWT_SECRET_KEY'):
    raise ValueError("Ошибка: Отсутствуют FLASK_SECRET_KEY или JWT_SECRET_KEY в .env файле")

# ✅ Создаем ОДИН экземпляр Flask
app = Flask(__name__)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))# Формируем путь к базе данных
instance_path = os.path.join(base_dir, 'instance')
db_path = os.path.join(instance_path, 'arenalink.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback_secret')



# Инициализация базы данных с привязкой к приложению
db.init_app(app)

# Настройка CORS с поддержкой куки
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

# Consolidated Logout Route
@app.route('/logout', methods=['POST', 'OPTIONS'])
def user_logout():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight accepted"}), 200
    response = jsonify({"message": "Logged out successfully"})
    response.delete_cookie("auth_token")
    return response, 200

# Получаем SECRET_KEY для токенов
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Функция для генерации JWT токена
def create_jwt(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Папка для загрузки файлов
UPLOAD_FOLDER = 'instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ✅ Первый эндпоинт для проверки токена
@app.route('/check-auth', methods=['GET', 'OPTIONS'])
def check_auth():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight for check-auth accepted"})
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200

    token = request.cookies.get('auth_token')
    if not token:
        return jsonify({'authenticated': False, 'error': 'No token found'}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'authenticated': False, 'error': 'User not found'}), 401

        return jsonify({
            'authenticated': True,
            'user_id': user.id,
            'role': user.role,
            'user_name': user.name
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'authenticated': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'authenticated': False, 'error': 'Invalid token'}), 401


# ✅ Второй эндпоинт для проверки активности
@app.route('/check-auth-status', methods=['GET'])
def check_auth_status():
    return jsonify({"message": "Check-auth endpoint is active"}), 200






# Эндпоинт для проверки выдачи токена
@app.route('/token-test', methods=['GET'])
def token_test():
    token = request.cookies.get("auth_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({"valid": True, "user_id": payload.get("user_id"), "role": payload.get("role")}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"valid": False, "error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"valid": False, "error": "Invalid token"}), 401
    return jsonify({"valid": False, "error": "No token found"}), 401

# Декоратор для проверки и извлечения user_id из JWT
def get_user_from_token():
    token = request.cookies.get("auth_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# ✅ Эндпоинт для обработки preflight-запросов (устранение ошибки 404 на OPTIONS /login)
@app.route('/login', methods=['OPTIONS'])
def login_options():
    response = jsonify({"message": "Preflight for login accepted"})
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response, 200



# ------------------------ РЕГИСТРАЦИЯ И ЛОГИН ------------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data format'}), 400

    existing_user = User.query.filter_by(login=data['login']).first()
    if existing_user:
        return jsonify({'error': 'This login is already taken'}), 400

    new_user = User(
        login=data['login'],
        name=data['name'],
        password=data['password'],
        role='fan',
        email=data.get('email', None),  # 📧 Добавлено email (может быть пустым)
        date_create=datetime.now(),
        date_update=datetime.now()
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Fan registered successfully!'}), 201



@app.route('/register_organizer', methods=['POST'])
def register_organizer():
    if 'documents' not in request.files:
        return jsonify({'error': 'File is required'}), 400

    file = request.files['documents']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    data = request.form
    existing_user = User.query.filter_by(login=data['login']).first()
    if existing_user:
        return jsonify({'error': 'This login is already taken'}), 400

    new_organizer = User(
        login=data['login'],
        name=data['organization'],
        password=data['password'],
        role='organizer',
        contact=data['contact'],
        file=file_path
    )
    db.session.add(new_organizer)
    db.session.commit()
    return jsonify({'message': 'Organizer registered successfully!'}), 201


# Эндпоинт для входа (обновлен с куки-сохранением)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    if user and user.password == data['password']:
        token = create_jwt(user.id, user.role)
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=False,       # Для локального теста
            samesite='Lax',     # Lax лучше для CORS при переходах
            path='/',           # Устанавливаем корневой путь
            max_age=180
        )
        print(f"Auth token set in cookie for user {user.id}")
        return response, 200
    return jsonify({"error": "Invalid login or password"}), 401

# Эндпоинт для добавления данных к пользователю с использованием user_id из токена
@app.route('/user/data', methods=['POST'])
def add_user_data():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.additional_info = data.get('additional_info')
        db.session.commit()
        return jsonify({"message": "Data added successfully"}), 200
    return jsonify({"error": "User not found"}), 404



# ------------------------ РАБОТА С МАТЧАМИ ------------------------

@app.route('/matches', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    result = [
        {
            'id': m.match_id,
            'name': m.match_name,
            'stadium': m.stadium_name,
            'date': m.date_time.strftime('%Y-%m-%d %H:%M'),
            'ticket_price': str(m.ticket_price)
        }
        for m in matches
    ]
    return jsonify(result), 200


@app.route('/get_match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get(match_id)
    
    # ✅ Добавляем проверку на отсутствие матча или даты
    if not match or not match.date_time:
        return jsonify({'error': 'Match not found or date missing'}), 404

    return jsonify({
        'id': match.match_id,
        'name': match.match_name,
        'date': match.date_time.strftime('%Y-%m-%dT%H:%M'),
        'stadium': match.stadium_name,
        'match_type': match.match_type,
        'ticket_quantity': match.ticket_quantity,
        'ticket_price': str(match.ticket_price)
    }), 200



@app.route('/add_match', methods=['POST'])
def add_match():
    user_id = get_user_from_token()  # ✅ Проверяем токен
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        if 'stadium_plan' not in request.files:
            return jsonify({'error': 'Stadium plan is required'}), 400

        file = request.files['stadium_plan']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        data = request.form

        new_match = Match(
            match_name=data.get('match_name'),
            date_time=datetime.strptime(data.get('date_time'), '%Y-%m-%dT%H:%M'),
            stadium_name=data.get('stadium_name'),
            stadium_plan=file_path,
            match_type=data.get('match_type'),
            ticket_quantity=int(data.get('ticket_quantity')),
            ticket_price=float(data.get('ticket_price')),
            created_by=user_id  # ✅ Используем user_id из токена
        )
        db.session.add(new_match)
        db.session.commit()
        return jsonify({'message': 'Match added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add match', 'details': str(e)}), 500




@app.route('/update_match', methods=['POST'])
def update_match():
    data = request.form
    match_id = data.get('match_id')
    match = Match.query.get(match_id)

    if not match:
        return jsonify({'error': 'Match not found'}), 404

    match.match_name = data['match_name']
    match.date_time = datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M')
    match.stadium_name = data['stadium_name']
    match.match_type = data['match_type']
    match.ticket_quantity = int(data['ticket_quantity'])
    match.ticket_price = float(data['ticket_price'])

    db.session.commit()
    return jsonify({'message': 'Match updated successfully!'}), 200


# ------------------------ Бронирование матча ------------------------

@app.route('/book_match', methods=['POST'])
def book_match():
    data = request.get_json()
    user_id = data.get('user_id')
    match_id = data.get('match_id')

    if not user_id or not match_id:
        return jsonify({'error': 'Missing user or match ID'}), 400

    match = Match.query.get(match_id)
    user = User.query.get(user_id)  # Получаем пользователя

    if not match or not user:
        return jsonify({'error': 'Match or User not found'}), 404

    if match.ticket_quantity <= 0:
        return jsonify({'error': 'No tickets available'}), 400

    existing_ticket = Ticket.query.filter_by(match_id=match_id, current_owner=user_id).first()
    if existing_ticket:
        return jsonify({'error': 'You have already booked this match!'}), 400

    match.ticket_quantity -= 1
    new_ticket = Ticket(match_id=match_id, current_owner=user_id, status='reserved')
    db.session.add(new_ticket)
    db.session.commit()

    # 📨 Отправка email пользователю
    if user.email:
        subject = "🎟 Ticket Booking Confirmation"
        body = f"""
        Hello {user.name}, 
        
        You have successfully booked a ticket for:
        🏟 Match: {match.match_name}
        📅 Date: {match.date_time.strftime('%Y-%m-%d %H:%M')}
        🏟 Stadium: {match.stadium_name}

        Thank you for choosing ArenaLink!
        """
        send_email(user.email, subject, body)

    return jsonify({'message': 'Match booked successfully!'}), 201



@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    user_id = data.get('user_id')
    match_id = data.get('match_id')

    if not user_id or not match_id:
        return jsonify({'error': 'Missing user or match ID'}), 400

    ticket = Ticket.query.filter_by(match_id=match_id, current_owner=user_id).first()
    user = User.query.get(user_id)  # Получаем пользователя
    match = Match.query.get(match_id)

    if not ticket or not user or not match:
        return jsonify({'error': 'No booking found for this match'}), 404

    match.ticket_quantity += 1
    db.session.delete(ticket)
    db.session.commit()

    # 📨 Отправка email пользователю
    if user.email:
        subject = "🚫 Ticket Cancellation Confirmation"
        body = f"""
        Hello {user.name},

        You have successfully **cancelled** your ticket for:
        🏟 Match: {match.match_name}
        📅 Date: {match.date_time.strftime('%Y-%m-%d %H:%M')}
        🏟 Stadium: {match.stadium_name}

        Your ticket has been refunded.

        Best regards,  
        ArenaLink Team
        """
        send_email(user.email, subject, body)

    return jsonify({'success': True, 'message': 'Booking cancelled successfully'}), 200




# ------------------------ ПОКАЗ ЗАБРОНИРОВАННОГО ------------------------
@app.route('/my_matches/<int:user_id>', methods=['GET'])
def my_matches(user_id):
    tickets = Ticket.query.filter_by(current_owner=user_id, status='reserved').all()
    matches = [Match.query.get(ticket.match_id) for ticket in tickets]

    result = [
        {
            'id': match.match_id,
            'name': match.match_name,
            'stadium': match.stadium_name,
            'date': match.date_time.strftime('%Y-%m-%d %H:%M')
        } for match in matches if match is not None
    ]
    return jsonify(result), 200

# ------------------------ ОТПРАВКА ПИСЕМ ------------------------

def send_email(to_email, subject, body):
    sender_email = "arenalink@yandex.ru"
    sender_password = "rzqkhuooosggqskq"
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# ------------------------ ЗАПУСК СЕРВЕРА ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)