from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def role_required(role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            if user['role'] != role:
                return jsonify({'message': 'Access denied'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

artist_required = role_required('Artist')
collector_required = role_required('Collector')