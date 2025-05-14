import os
from flask import Flask, request, jsonify, Response, make_response, session
from flask_cors import CORS
from models import db, User, Match, Ticket
from datetime import datetime,  timedelta, UTC
import jwt
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import pandas as pd
from io import BytesIO
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import Stadium, Sector, Row
from flask import send_from_directory





# Загружаем переменные окружения из .env файла
load_dotenv()

# Проверяем наличие ключей в переменных окружения
if not os.getenv('FLASK_SECRET_KEY') or not os.getenv('JWT_SECRET_KEY'):
    raise ValueError("Ошибка: Отсутствуют FLASK_SECRET_KEY или JWT_SECRET_KEY в .env файле")

# ✅ Создаем ОДИН экземпляр Flask
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, static_folder='static')
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))# Формируем путь к базе данных
instance_path = os.path.join(base_dir, 'instance')
db_path = os.path.join(instance_path, 'arenalink.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback_secret')



# Инициализация базы данных с привязкой к приложению
db.init_app(app)

def initialize_schema_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    with db.engine.connect() as connection:
        connection.connection.executescript(sql_script)  # для SQLite

# Выполняем загрузку схемы один раз, внутри app context
with app.app_context():
    db.create_all()
    if not db.session.query(Stadium).filter_by(id=1).first():
        initialize_schema_from_file('instance/stadium_schema.sql')




from flask import Flask, request
from datetime import datetime




# Пример функции фильтрации, как она будет выглядеть в app.py
def filter_matches_query(base_query):
    # Извлекаем параметры фильтрации из запроса
    name = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    after_date = request.args.get('after_date')
    before_date = request.args.get('before_date')

    # Применяем фильтры по условию
    if name:
        base_query = base_query.filter(
            (Match.match_name.ilike(f'%{name}%')) |
            (Match.stadium_name.ilike(f'%{name}%'))
        )
    if min_price is not None:
        base_query = base_query.filter(Match.ticket_price >= min_price)
    if max_price is not None:
        base_query = base_query.filter(Match.ticket_price <= max_price)
    if after_date:
        base_query = base_query.filter(Match.date_time >= datetime.fromisoformat(after_date))
    if before_date:
        base_query = base_query.filter(Match.date_time <= datetime.fromisoformat(before_date))

    return base_query

"Это будет вставлено в endpoint /matches перед .all()"


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
    response.headers.add('Access-Control-Allow-Credentials', 'true')
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
    email=data.get('email'),  # <-- добавлено
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
        response = make_response(jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "role": user.role,
            "user_name": user.name
        }))
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/',
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

@app.route('/organizer/matches', methods=['GET'])
def get_organizer_matches():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    matches = Match.query.filter_by(created_by=user_id).all()
    result = [
        {
            'id': m.match_id,
            'match_name': m.match_name,
            'stadium_name': m.stadium_name,
            'date_time': m.date_time.strftime('%Y-%m-%d %H:%M'),
            'ticket_quantity': m.ticket_quantity,
            'ticket_price': float(m.ticket_price)
        }
        for m in matches
    ]
    return jsonify(result), 200



@app.route('/matches', methods=['GET'])
@app.route('/matches', methods=['GET'])
def get_matches():
    query = Match.query

    # Получаем параметры фильтрации
    name = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    after_date = request.args.get('after_date')
    before_date = request.args.get('before_date')

    if name:
        query = query.filter(
            (Match.match_name.ilike(f'%{name}%')) |
            (Match.stadium_name.ilike(f'%{name}%'))
        )
    if min_price is not None:
        query = query.filter(Match.ticket_price >= min_price)
    if max_price is not None:
        query = query.filter(Match.ticket_price <= max_price)
    if after_date:
        query = query.filter(Match.date_time >= datetime.fromisoformat(after_date))
    if before_date:
        query = query.filter(Match.date_time <= datetime.fromisoformat(before_date))

    matches = query.all()

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
        'ticket_price': str(match.ticket_price),
        'created_by': match.created_by,
        'stadium_image': match.stadium_image
    }), 200



@app.route('/add_match', methods=['POST'])
def add_match():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.form
        # Проверка на дубликат матча
        existing_match = Match.query.filter_by(
            match_name=data.get('match_name'),
            date_time=datetime.strptime(data.get('date_time'), '%Y-%m-%dT%H:%M'),
            created_by=user_id
        ).first()

        if existing_match:
            return jsonify({'error': 'Match with this name and time already exists.'}), 400

        stadium_choice = data.get('stadium_choice')
        stadium_plan_path = None
        stadium_image_path = None

        if stadium_choice == 'arenalink':
            stadium_id = 1
            stadium_name = 'ArenaLink Stadium'
            stadium_plan_path = None
            stadium_image_path = '/static/images/arenalink_stadium.jpg'
        else:
            stadium_id = None
            stadium_name = data.get('stadium_name')

            if 'stadium_plan' in request.files:
                plan_file = request.files['stadium_plan']
                if plan_file and plan_file.filename.endswith('.csv'):
                    stadium_plan_path = os.path.join(app.config['UPLOAD_FOLDER'], plan_file.filename)
                    plan_file.save(stadium_plan_path)

            if 'stadium_image' in request.files:
                image_file = request.files['stadium_image']
                if image_file and image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    stadium_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
                    image_file.save(stadium_image_path)

        new_match = Match(
            match_name=data.get('match_name'),
            date_time=datetime.strptime(data.get('date_time'), '%Y-%m-%dT%H:%M'),
            stadium_name=stadium_name,
            stadium_plan=stadium_plan_path,
            stadium_image=stadium_image_path,
            match_type=data.get('match_type'),
            ticket_quantity=int(data.get('ticket_quantity', 0)),
            ticket_price=float(data.get('ticket_price', 0)),  # используется как default
            created_by=user_id
        )
        db.session.add(new_match)
        db.session.flush()  # получаем match_id

        # 🧩 Если выбран ArenaLink Stadium — сохраняем цены по секторам
        if stadium_choice == 'arenalink':
            sectors = Sector.query.filter_by(stadium_id=1).all()
            for sector in sectors:
                price_field = f'sector_price_{sector.name}'
                if price_field in data:
                    ticket_count = 0
                    for row in sector.rows:
                        ticket_count += row.seat_count
                        for seat_num in range(1, row.seat_count + 1):
                            ticket = Ticket(
                                match_id=new_match.match_id,
                                sector=sector.name,
                                row=row.number,
                                seat=seat_num,
                                price=float(data[price_field]),
                                current_owner=None,
                                status='available'
                            )
                            db.session.add(ticket)
                    new_match.ticket_quantity += ticket_count

        db.session.commit()
        return jsonify({'message': 'Match added successfully!'}), 201

    except Exception as e:
        print(f"❌ ERROR while adding match: {e}")  # <-- это напечатает ошибку в терминал
        db.session.rollback()
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
    match.ticket_quantity = int(data['ticket_quantity'])
    match.ticket_price = float(data['ticket_price'])

    # Обновляем match_type только если оно передано
    if 'match_type' in data:
        match.match_type = data['match_type']

    db.session.commit()
    return jsonify({'message': 'Match updated successfully!'}), 200


# ------------------------ Отправка отчета о матчах для организатора ------------------------
@app.route('/send_report_by_login/<string:login>', methods=['POST'])
def send_report_by_login(login):
    user = User.query.filter_by(login=login).first()
    if not user or user.role != 'organizer':
        return jsonify({'error': 'Organizer not found'}), 404
    if not user.email:
        return jsonify({'error': 'Email is not specified for the organizer'}), 400

    matches = Match.query.filter_by(created_by=user.id).all()
    if not matches:
        return jsonify({'error': 'No matches found for this organizer'}), 404

    # English column names
    data = [{
        'Match Name': m.match_name,
        'Date & Time': m.date_time.strftime('%Y-%m-%d %H:%M'),
        'Stadium': m.stadium_name,
        'Match Type': m.match_type.capitalize(),
        'Tickets Left': m.ticket_quantity,
        'Ticket Price (₽)': float(m.ticket_price)
    } for m in matches]

    df = pd.DataFrame(data)

    subject = "📊 Match Report"
    body = (
        f"Hello {user.name},\n\n"
        f"Attached is your match report in Excel format.\n\n"
        f"Best regards,\nArenaLink Team"
    )

    send_email_with_excel(user.email, subject, body, df)

    return jsonify({'message': 'The match report was successfully sent to the organizer\'s email'}), 200

@app.route('/api/sectors/<int:stadium_id>', methods=['GET'])
def get_sectors_by_stadium(stadium_id):
    sectors = Sector.query.filter_by(stadium_id=stadium_id).all()
    return jsonify({
        "sectors": [s.name for s in sectors]
    })







# ------------------------ Бронирование матча ------------------------

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        ticket_id = data.get('ticket_id')

        ticket = Ticket.query.get(ticket_id)
        if not ticket or ticket.status != 'available':
            return jsonify({'error': 'Ticket not available'}), 400

        ticket.current_owner = user_id
        ticket.status = 'reserved'
        ticket.date_update = datetime.utcnow()
        db.session.commit()

        user = User.query.get(user_id)
        match = Match.query.get(ticket.match_id)

        if user and user.email:
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

        return jsonify({'message': 'Ticket booked successfully!'})

    except Exception as e:
        print(f"❌ Booking failed: {e}")  # <-- важно!
        return jsonify({'error': 'Booking failed', 'details': str(e)}), 500





@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    user_id = get_user_from_token()

    if not ticket_id or not user_id:
        return jsonify({'error': 'Missing ticket or user ID'}), 400

    ticket = Ticket.query.get(ticket_id)
    if not ticket or ticket.current_owner != user_id:
        return jsonify({'error': 'Booking not found'}), 404

    user = User.query.get(user_id)
    match = Match.query.get(ticket.match_id)

    ticket.status = 'available'
    ticket.current_owner = None
    ticket.date_update = datetime.utcnow()
    db.session.commit()

    # 📨 Отправка email
    if user and user.email:
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

    return jsonify({'message': 'Booking cancelled'}), 200


@app.route('/available_tickets/<int:match_id>', methods=['GET'])
def available_tickets(match_id):
    tickets = Ticket.query.filter_by(match_id=match_id, status='available').all()
    result = [{
        'ticket_id': t.ticket_id,
        'sector': t.sector,
        'row': t.row,
        'seat': t.seat,
        'price': float(t.price or 0)
    } for t in tickets]
    return jsonify({'tickets': result})



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

def send_email_with_excel(to_email, subject, body, df: pd.DataFrame, filename="report.xlsx"):
    sender_email = "arenalink@yandex.ru"
    sender_password = "rzqkhuooosggqskq"
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    # Сохраняем Excel в память
    excel_stream = BytesIO()
    df.to_excel(excel_stream, index=False)
    excel_stream.seek(0)

    attachment = MIMEApplication(excel_stream.read(), _subtype='xlsx')
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email with Excel sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email with Excel: {e}")

def send_email(to_email, subject, body):
    sender_email = "arenalink@yandex.ru"
    sender_password = "rzqkhuooosggqskq"
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# ------------------------ смена имени и пароля ------------------------

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'password' in data:
        user.password = data['password']
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200



# ------------------------ ЗАПУСК СЕРВЕРА ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)