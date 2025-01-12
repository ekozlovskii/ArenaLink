from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users]
    return jsonify(user_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
