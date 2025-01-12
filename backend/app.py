from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
from models import db, User

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

    # Ищем пользователя в базе данных
    user = User.query.filter_by(login=login, password=password).first()
    if user:
        return jsonify({'message': 'Login successful!', 'role': user.role}), 200
    else:
        return jsonify({'error': 'Invalid login or password'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)