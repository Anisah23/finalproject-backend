from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import User, db

def role_required(*roles):
    """
    Decorator to check if user has required role(s).
    Accepts multiple roles for flexibility.
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                user = User.query.get(user_id)

                if not user:
                    return jsonify({'message': 'User not found'}), 404

                if user.role not in roles:
                    return jsonify({
                        'message': f'Access denied. Required role(s): {", ".join(roles)}. Your role: {user.role}'
                    }), 403

                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Role check error: {str(e)}")
                return jsonify({'message': 'Authentication error'}), 500
        return wrapper
    return decorator

def admin_required(f):
    """Decorator for admin-only access"""
    return role_required('admin')(f)

def artist_required(f):
    """Decorator for artist access"""
    return role_required('artist')(f)

def collector_required(f):
    """Decorator for collector access"""
    return role_required('collector')(f)

def artist_or_admin_required(f):
    """Decorator for artist or admin access"""
    return role_required('artist', 'admin')(f)

def collector_or_admin_required(f):
    """Decorator for collector or admin access"""
    return role_required('collector', 'admin')(f)

def get_current_user():
    """Helper function to get current user from JWT token"""
    try:
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return None

def create_token_payload(user):
    """Create JWT payload for user"""
    return {
        'user_id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'is_verified': user.is_verified
    }