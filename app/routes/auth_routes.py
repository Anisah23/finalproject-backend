from flask import Blueprint, request, jsonify
from app.models import User
from app import db, bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'collector')  

    if User.query.filter((User.username==username) | (User.email==email)).first():
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'{role.capitalize()} registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user and bcrypt.check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'access_token': access_token, 'role': user.role}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
