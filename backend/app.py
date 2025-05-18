import os
from flask import Flask, request, jsonify, Response, make_response, session, send_from_directory, render_template
from flask_cors import CORS
from models import db, User, Match, Ticket, TicketHistory, Stadium, Sector, Row
from datetime import datetime, timedelta, UTC
import jwt
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import pandas as pd
from io import BytesIO
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import webbrowser
import threading

# Загружаем переменные окружения из .env файла
load_dotenv()

# Проверяем наличие ключей в переменных окружения
if not os.getenv('FLASK_SECRET_KEY') or not os.getenv('JWT_SECRET_KEY'):
    raise ValueError("Ошибка: Отсутствуют FLASK_SECRET_KEY или JWT_SECRET_KEY в .env файле")

# ✅ Создаем экземпляр Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# Разрешаем CORS
CORS(app, supports_credentials=True, origins="http://127.0.0.1:5500")

# Конфигурация базы данных
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
instance_path = os.path.join(base_dir, 'instance')
db_path = os.path.join(instance_path, 'arenalink.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallback_secret')

# Инициализация базы данных
db.init_app(app)

def initialize_schema_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    with db.engine.connect() as connection:
        connection.connection.executescript(sql_script)  # для SQLite

with app.app_context():
    db.create_all()
    if not db.session.query(Stadium).filter_by(id=1).first():
        initialize_schema_from_file('instance/stadium_schema.sql')

# Функция для фильтрации матчей
def filter_matches_query(base_query):
    name = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    after_date = request.args.get('after_date')
    before_date = request.args.get('before_date')

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

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# ------------------------ HTML Рендеринг ------------------------

@app.route('/')
def main_logit_page():
    return render_template('main_logit_page.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login-step2')
def login_step2_page():
    return render_template('login-step2.html')

@app.route('/fan-dashboard')
def fan_dashboard():
    return render_template('fan-dashboard.html')

@app.route('/fan-matches')
def fan_matches():
    return render_template('fan-matches.html')

@app.route('/fan-settings')
def fan_settings():
    return render_template('fan-settings.html')

@app.route('/fan-registration')
def fan_registration():
    return render_template('fan-registration.html')

@app.route('/organizer-dashboard')
def organizer_dashboard():
    return render_template('organizer-dashboard.html')

@app.route('/organizer-page')
def organizer_page():
    return render_template('organizer-page.html')

@app.route('/settings-orgonizer')
def settings_organizer():
    return render_template('settings-orgonizer.html')

@app.route('/add-match')
def add_match_page():
    return render_template('add-match.html')

@app.route('/edit-match')
def edit_match_page():
    return render_template('edit-match.html')

@app.route('/match-details')
def match_details_page():
    return render_template('match-details.html')

@app.route('/my-matches')
def my_matches_page():
    return render_template('my-matches.html')


# ---- JWT и Аутентификация ----

from flask import render_template  # Добавляем, если ты хочешь позже отдавать HTML

# Получаем секретный ключ для токенов
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Генерация JWT токена
def create_jwt(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Проверка токена из cookies
def get_user_from_token():
    token = request.cookies.get("auth_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

# Preflight для логина
@app.route('/login', methods=['OPTIONS'])
def login_options():
    response = jsonify({"message": "Preflight for login accepted"})
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 200

# Logout + удаление куки
@app.route('/logout', methods=['POST', 'OPTIONS'])
def user_logout():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight accepted"}), 200
    response = jsonify({"message": "Logged out successfully"})
    response.delete_cookie("auth_token")
    return response, 200

# Проверка JWT-токена и возвращение информации о пользователе
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

# Проверка активности / тестовый пинг
@app.route('/check-auth-status', methods=['GET'])
def check_auth_status():
    return jsonify({"message": "Check-auth endpoint is active"}), 200

# Простой тест токена
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




# ------------------------ РЕГИСТРАЦИЯ И ЛОГИН ------------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data or 'name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'This login is already taken'}), 400

    new_user = User(
        login=data['login'],
        name=data['name'],
        password=data['password'],
        role='fan',
        email=data.get('email'),
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
    required_fields = ['login', 'password', 'organization', 'contact']
    if any(field not in data for field in required_fields):
        return jsonify({'error': 'Missing required form fields'}), 400

    if User.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'This login is already taken'}), 400

    new_organizer = User(
        login=data['login'],
        name=data['organization'],
        password=data['password'],
        role='organizer',
        contact=data['contact'],
        email=data.get('email'),
        file=file_path,
        date_create=datetime.now(),
        date_update=datetime.now()
    )
    db.session.add(new_organizer)
    db.session.commit()
    return jsonify({'message': 'Organizer registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'error': 'Missing login or password'}), 400

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
            max_age=3600  # 1 час
        )
        print(f"✅ Auth token set for user {user.login}")
        return response, 200

    return jsonify({"error": "Invalid login or password"}), 401


@app.route('/user/data', methods=['POST'])
def add_user_data():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.additional_info = data.get('additional_info')
    user.date_update = datetime.now()
    db.session.commit()
    return jsonify({"message": "Data added successfully"}), 200



# ------------------------ РАБОТА С МАТЧАМИ ------------------------

@app.route('/organizer/matches', methods=['GET'])
def get_organizer_matches():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    matches = Match.query.filter_by(created_by=user_id).all()
    result = []

    for match in matches:
        sold_or_reserved = Ticket.query.filter(
            Ticket.match_id == match.match_id,
            Ticket.status.in_(['sold', 'reserved'])
        ).count()

        result.append({
            'id': match.match_id,
            'match_name': match.match_name,
            'stadium_name': match.stadium_name,
            'date_time': match.date_time.strftime('%Y-%m-%d %H:%M'),
            'match_type': match.match_type,
            'tickets_sold': sold_or_reserved,
            'ticket_quantity': match.ticket_quantity
        })

    return jsonify(result), 200



@app.route('/matches', methods=['GET'])
def get_matches():
    query = Match.query

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
        try:
            query = query.filter(Match.date_time >= datetime.fromisoformat(after_date))
        except ValueError:
            return jsonify({'error': 'Invalid after_date format'}), 400
    if before_date:
        try:
            query = query.filter(Match.date_time <= datetime.fromisoformat(before_date))
        except ValueError:
            return jsonify({'error': 'Invalid before_date format'}), 400

    matches = query.all()

    result = [
        {
            'id': match.match_id,
            'name': match.match_name,
            'stadium': match.stadium_name,
            'date': match.date_time.strftime('%Y-%m-%d %H:%M'),
            'ticket_price': str(match.ticket_price)
        }
        for match in matches
    ]
    return jsonify(result), 200


@app.route('/get_match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get(match_id)

    if not match or not match.date_time:
        return jsonify({'error': 'Match not found or date missing'}), 404

    # Собираем цены по каждому сектору
    sector_prices = {}
    tickets = Ticket.query.filter_by(match_id=match_id).all()
    for ticket in tickets:
        if ticket.sector and ticket.price is not None:
            sector_prices[ticket.sector] = float(ticket.price)

    return jsonify({
        'id': match.match_id,
        'name': match.match_name,
        'date': match.date_time.strftime('%Y-%m-%dT%H:%M'),
        'stadium': match.stadium_name,
        'match_type': match.match_type,
        'ticket_quantity': match.ticket_quantity,
        'sector_prices': sector_prices,
        'created_by': match.created_by,
        'organizer_login': match.created_by_user.login,  # 👈 добавляем
        'stadium_image': match.stadium_image
    }), 200






@app.route('/add_match', methods=['POST'])
def add_match():
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.form
        match_name = data.get('match_name')
        date_time = datetime.strptime(data.get('date_time'), '%Y-%m-%dT%H:%M')

        # Проверка на дубликат матча
        existing_match = Match.query.filter_by(
            match_name=match_name,
            date_time=date_time,
            created_by=user_id
        ).first()
        if existing_match:
            return jsonify({'error': 'Match with this name and time already exists.'}), 400

        stadium_choice = data.get('stadium_choice')
        stadium_name = None
        stadium_plan_path = None
        stadium_image_path = None

        if stadium_choice == 'arenalink':
            stadium_name = 'ArenaLink Stadium'
            stadium_image_path = '/static/images/arenalink_stadium.jpg'
        else:
            stadium_name = data.get('stadium_name')
            if 'stadium_plan' in request.files:
                plan_file = request.files['stadium_plan']
                if plan_file.filename.endswith('.csv'):
                    stadium_plan_path = os.path.join(app.config['UPLOAD_FOLDER'], plan_file.filename)
                    plan_file.save(stadium_plan_path)

            if 'stadium_image' in request.files:
                image_file = request.files['stadium_image']
                if image_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    stadium_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
                    image_file.save(stadium_image_path)

        new_match = Match(
            match_name=match_name,
            date_time=date_time,
            stadium_name=stadium_name,
            stadium_plan=stadium_plan_path,
            stadium_image=stadium_image_path,
            match_type=data.get('match_type'),
            ticket_quantity=0,
            ticket_price=float(data.get('ticket_price', 0)),
            created_by=user_id
        )
        db.session.add(new_match)
        db.session.flush()

        # Если выбран ArenaLink Stadium — добавим билеты по секторам
        if stadium_choice == 'arenalink':
            sectors = Sector.query.filter_by(stadium_id=1).all()
            for sector in sectors:
                price_field = f'sector_price_{sector.name}'
                if price_field in data:
                    sector_price = float(data[price_field])
                    for row in sector.rows:
                        for seat_num in range(1, row.seat_count + 1):
                            db.session.add(Ticket(
                                match_id=new_match.match_id,
                                sector=sector.name,
                                row=row.number,
                                seat=seat_num,
                                price=sector_price,
                                current_owner=None,
                                status='available'
                            ))
                            new_match.ticket_quantity += 1

        db.session.commit()
        return jsonify({'message': 'Match added successfully!'}), 201

    except Exception as e:
        print(f"❌ ERROR while adding match: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to add match', 'details': str(e)}), 500


@app.route('/update_match', methods=['POST'])
def update_match():
    data = request.form
    match_id = data.get('match_id')
    match = Match.query.get(match_id)

    if not match:
        return jsonify({'error': 'Match not found'}), 404

    try:
        match.match_name = data['match_name']
        match.date_time = datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M')
        match.stadium_name = data['stadium_name']
        match.match_type = data.get('match_type', match.match_type)
        match.ticket_quantity = int(data['ticket_quantity'])

        # Удаляем старые sector_price
        SectorPrice.query.filter_by(match_id=match.match_id).delete()

        # Добавляем новые sector_price из формы
        for key in data:
            if key.startswith('sector_price_'):
                sector = key.replace('sector_price_', '')
                price = float(data[key])
                db.session.add(SectorPrice(
                    match_id=match.match_id,
                    sector=sector,
                    price=price
                ))

        db.session.commit()
        return jsonify({'message': 'Match updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update match', 'details': str(e)}), 500



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

    import io
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for match in matches:
            all_tickets = Ticket.query.filter_by(match_id=match.match_id).all()
            total = len(all_tickets)
            occupied = sum(1 for t in all_tickets if t.status in ['sold', 'reserved'])
            revenue = sum(float(t.price or 0) for t in all_tickets if t.status == 'sold')  # revenue = только sold
            fill = f"{round((occupied / total) * 100)}%" if total else "0%"
            avg_price = round(revenue / occupied, 2) if occupied else 0

            rows = [{
                'Match Name': match.match_name,
                'Date & Time': match.date_time.strftime('%Y-%m-%d %H:%M'),
                'Stadium': match.stadium_name,
                'Match Type': (match.match_type or '').capitalize(),
                'Tickets Used': f'{occupied}/{total}',
                'Fill %': fill,
                'Total Revenue (₽)': round(revenue, 2),
                'Average Ticket Price (₽)': avg_price
            }]

            # Статистика по секторам
            sector_data = {}
            for t in all_tickets:
                if not t.sector:
                    continue
                if t.sector not in sector_data:
                    sector_data[t.sector] = {'occupied': 0, 'total': 0, 'revenue': 0.0}
                sector_data[t.sector]['total'] += 1
                if t.status in ['sold', 'reserved']:
                    sector_data[t.sector]['occupied'] += 1
                if t.status == 'sold':
                    sector_data[t.sector]['revenue'] += float(t.price or 0)

            for sector, info in sorted(sector_data.items()):
                occ = info['occupied']
                tot = info['total']
                rev = info['revenue']
                fill_s = f"{round((occ / tot) * 100)}%" if tot else "0%"
                avg_s = round(rev / occ, 2) if occ else 0

                rows.append({
                    'Match Name': f'↳ Sector {sector}',
                    'Date & Time': '',
                    'Stadium': '',
                    'Match Type': '',
                    'Tickets Used': f"{occ}/{tot}",
                    'Fill %': fill_s,
                    'Total Revenue (₽)': round(rev, 2),
                    'Average Ticket Price (₽)': avg_s
                })

            df = pd.DataFrame(rows)
            sheet_name = match.match_name[:31].replace('/', '_').replace('\\', '_')
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    output.seek(0)

    subject = "📊 Match Report (Multi-Sheet)"
    body = f"Hello {user.name},\n\nAttached is your match report with sector stats on separate sheets.\n\nBest regards,\nArenaLink Team"

    send_email_with_excel(user.email, subject, body, output, filename="match_report.xlsx")
    return jsonify({'message': '📩 Report successfully sent'}), 200





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
        if not ticket_id:
            return jsonify({'error': 'ticket_id is required'}), 400

        ticket = Ticket.query.get(ticket_id)
        if not ticket or ticket.status != 'available':
            return jsonify({'error': 'Ticket not available'}), 400

        ticket.current_owner = user_id
        ticket.status = 'reserved'
        ticket.date_update = datetime.utcnow()

        history = TicketHistory(
            ticket_id=ticket.ticket_id,
            previous_owner=None,
            new_owner=user_id,
            status='sold',
            date_create=datetime.utcnow()
        )
        db.session.add(history)
        db.session.commit()

        user = User.query.get(user_id)
        match = Match.query.get(ticket.match_id)

        # Отправка письма (если есть email)
        if user and user.email:
            subject = "🎟 Ticket Booking Confirmation"
            body = (
                f"Hello {user.name},\n\n"
                f"You have successfully booked a ticket for:\n"
                f"🏟 Match: {match.match_name}\n"
                f"📅 Date: {match.date_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"🏟 Stadium: {match.stadium_name}\n\n"
                f"Thank you for choosing ArenaLink!"
            )
            send_email(user.email, subject, body)

        return jsonify({'message': 'Ticket booked successfully!'})

    except Exception as e:
        print(f"❌ Booking failed: {e}")
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

    history = TicketHistory(
        ticket_id=ticket.ticket_id,
        previous_owner=user_id,
        new_owner=None,
        status='available',
        date_create=datetime.utcnow()
    )
    db.session.add(history)
    db.session.commit()

    if user and user.email:
        subject = "🚫 Ticket Cancellation Confirmation"
        body = (
            f"Hello {user.name},\n\n"
            f"You have successfully **cancelled** your ticket for:\n"
            f"🏟 Match: {match.match_name}\n"
            f"📅 Date: {match.date_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"🏟 Stadium: {match.stadium_name}\n\n"
            f"Your ticket has been refunded.\n\n"
            f"Best regards,\nArenaLink Team"
        )
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
    result = []

    for ticket in tickets:
        match = Match.query.get(ticket.match_id)
        if match:
            result.append({
                'ticket_id': ticket.ticket_id,
                'name': match.match_name,
                'stadium': match.stadium_name,
                'date': match.date_time.strftime('%Y-%m-%d %H:%M'),
                'sector': ticket.sector,
                'row': ticket.row,
                'seat': ticket.seat
            })

    return jsonify(result), 200



# ------------------------ ОТПРАВКА ПИСЕМ ------------------------

def send_email_with_excel(to_email, subject, body, excel_stream: BytesIO, filename="report.xlsx"):
    sender_email = "arenalink@yandex.ru"
    sender_password = "rzqkhuooosggqskq"
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    excel_stream.seek(0)  # 🔁 обязательно перед чтением
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

    if 'name' in data and data['name']:
        user.name = data['name']
    if 'password' in data and data['password']:
        user.password = data['password']

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200




# ------------------------ ЗАПУСК СЕРВЕРА ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    threading.Timer(1.0, open_browser).start()
    app.run(host='127.0.0.1', port=5000, debug=True)
