from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # Включаем CORS

db.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print('Received data:', data)

    if not data:
        return jsonify({'error': 'Invalid data format. Expected JSON'}), 400

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)