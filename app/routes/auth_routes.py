from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models import User, db
from app.utils.auth_utils import create_token_payload
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['full_name', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400

        full_name = data.get('full_name').strip()
        email = data.get('email').strip().lower()
        password = data.get('password')
        role = data.get('role').lower()

        # Validate email format
        if not validate_email(email):
            return jsonify({'message': 'Invalid email format'}), 400

        # Validate password strength
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            return jsonify({'message': password_message}), 400

        # Validate role
        if role not in ['artist', 'collector']:
            return jsonify({'message': 'Role must be either artist or collector'}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 409

        # Create new user
        new_user = User(
            full_name=full_name,
            email=email,
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Create JWT tokens
        token_payload = create_token_payload(new_user)
        access_token = create_access_token(identity=new_user.id, additional_claims=token_payload)
        refresh_token = create_refresh_token(identity=new_user.id)

        return jsonify({
            'message': f'{role.capitalize()} registered successfully',
            'user': new_user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Registration failed. Please try again.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400

        email = data.get('email').strip().lower()
        password = data.get('password')

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401

        # Check password
        if not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401

        # Create JWT tokens
        token_payload = create_token_payload(user)
        access_token = create_access_token(identity=user.id, additional_claims=token_payload)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed. Please try again.'}), 500

@auth_bp.route('/profile', methods=['GET'])
@auth_bp.route('/profile', methods=['PUT'])
def profile():
    # This will be implemented with proper authentication decorators
    return jsonify({'message': 'Profile endpoint - to be implemented'}), 501
