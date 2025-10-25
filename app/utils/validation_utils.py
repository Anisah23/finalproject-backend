import re
from flask import jsonify

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

def validate_price(price):
    try:
        return float(price) > 0
    except (ValueError, TypeError):
        return False

def validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({'message': f'Missing required fields: {", ".join(missing)}'}), 400
    return None