from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != required_role:
                return jsonify({'message': f'Access denied. {required_role.capitalize()} role required.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def artist_required(f):
    return role_required('Artist')(f)

def collector_required(f):
    return role_required('Collector')(f)