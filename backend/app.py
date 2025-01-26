from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
from models import db, User, Match
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arenalink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # Включаем CORS

db.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print('Received data:', data)

    if not data:
        return jsonify({'error': 'Invalid data format. Expected JSON'}), 400

    # Проверка уникальности login
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
    print('User added to database')
    return jsonify({'message': 'Fan registered successfully!'}), 201



UPLOAD_FOLDER = '/instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register_organizer', methods=['POST'])
def register_organizer():
    if 'documents' not in request.files:
        return jsonify({'error': 'File is required'}), 400

    file = request.files['documents']
    file_path = f'instance/uploads/{file.filename}'
    file.save(file_path)

    data = request.form
    print('Received form data:', data)

    # Проверка уникальности login
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
    print('Organizer added to database')
    return jsonify({'message': 'Organizer registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Find user in the database
    user = User.query.filter_by(login=login, password=password).first()
    if user:
        return jsonify({
            'message': 'Login successful!',
            'user_id': user.id,  # Return the user ID
            'role': user.role,
            'name': user.name
        }), 200
    else:
        return jsonify({'error': 'Invalid login or password'}), 401


@app.route('/add_match', methods=['POST'])
def add_match():
    if 'stadium_plan' not in request.files:
        return jsonify({'error': 'Stadium plan is required'}), 400

    file = request.files['stadium_plan']
    file_path = f'instance/uploads/{file.filename}'
    file.save(file_path)

    data = request.form
    new_match = Match(
        match_name=data['match_name'],
        date_time=datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M'),
        stadium_name=data['stadium_name'],
        stadium_plan=file_path,
        match_type=data['match_type'],
        ticket_quantity=int(data['ticket_quantity']),
        ticket_price=float(data['ticket_price']),
        created_by=1  # Replace with actual user ID
    )
    db.session.add(new_match)
    db.session.commit()

    return jsonify({'message': 'Match added successfully!'}), 201


@app.route('/my_matches', methods=['GET'])
def get_my_matches():
    matches = Match.query.all()
    print("Matches found:", matches)  # Debugging output

    matches_list = []
    for match in matches:
        matches_list.append({
            'id': match.match_id,
            'match_name': match.match_name,
            'date_time': match.date_time.strftime('%Y-%m-%d %H:%M'),
            'stadium_name': match.stadium_name,
            'match_type': match.match_type,
            'ticket_quantity': match.ticket_quantity,
            'ticket_price': str(match.ticket_price),
        })

    return jsonify(matches_list), 200

@app.route('/get_match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({'error': 'Match not found'}), 404

    return jsonify({
        'id': match.match_id,
        'match_name': match.match_name,
        'date_time': match.date_time.strftime('%Y-%m-%dT%H:%M'),
        'stadium_name': match.stadium_name,
        'match_type': match.match_type,
        'ticket_quantity': match.ticket_quantity,
        'ticket_price': str(match.ticket_price)
    }), 200


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

    if 'stadium_plan' in request.files:
        file = request.files['stadium_plan']
        file_path = f'instance/uploads/{file.filename}'
        file.save(file_path)
        match.stadium_plan = file_path

    db.session.commit()

    return jsonify({'message': 'Match updated successfully!'}), 200

@app.route('/update_organizer', methods=['POST'])
def update_organizer():
    data = request.get_json()
    user_id = data.get('user_id')
    new_name = data.get('name')
    new_password = data.get('password')

    organizer = User.query.filter_by(id=user_id, role='organizer').first()

    if not organizer:
        return jsonify({'error': 'Organizer not found'}), 404

    if new_name:
        organizer.name = new_name
    if new_password:
        organizer.password = new_password  # Ideally, hash passwords before storing

    db.session.commit()
    return jsonify({'message': 'Organizer settings updated successfully!'}), 200

@app.route('/get_organizer/<int:user_id>', methods=['GET'])
def get_organizer(user_id):
    organizer = User.query.filter_by(id=user_id, role='organizer').first()

    if not organizer:
        return jsonify({'error': 'Organizer not found'}), 404

    return jsonify({
        'name': organizer.name,
        'password': organizer.password  # In real applications, don't send passwords directly
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


