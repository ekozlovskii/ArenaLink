from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db, User, Match, Ticket
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arenalink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

CORS(app)
db.init_app(app)

# Папка для загрузки файлов
UPLOAD_FOLDER = 'instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        role='fan'
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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(login=data['login'], password=data['password']).first()
    if user:
        session['user_id'] = user.id  # ✅ Явно устанавливаем user_id
        session['user_role'] = user.role
        session.modified = True  # ✅ Гарантируем сохранение сессии

        return jsonify({
            'message': 'Login successful!',
            'user_id': user.id,
            'role': user.role,
            'name': user.name
        }), 200
    else:
        return jsonify({'error': 'Invalid login or password'}), 401



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

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
    if not match:
        return jsonify({'error': 'Match not found'}), 404

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
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized. Please log in again.'}), 401

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
            created_by=session['user_id']  # ✅ Используем user_id из сессии
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

# В app.py
@app.route('/book_match', methods=['POST'])
def book_match():
    data = request.get_json()
    user_id = data.get('user_id')
    match_id = data.get('match_id')

    print(f'Received user_id: {user_id}, match_id: {match_id}')  # ✅ Лог в консоли сервера

    if not user_id or not match_id:
        return jsonify({'error': 'Missing user or match ID'}), 400

    existing_ticket = Ticket.query.filter_by(match_id=match_id, current_owner=user_id).first()
    if existing_ticket:
        return jsonify({'message': 'Match already booked!'}), 200

    new_ticket = Ticket(
        match_id=match_id,
        current_owner=user_id,
        status='reserved'
    )
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'Match booked successfully!'}), 201


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


# ------------------------ ЗАПУСК СЕРВЕРА ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
