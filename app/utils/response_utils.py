from flask import jsonify

def success_response(message, data=None, status_code=200):
    response = {'success': True, 'message': message}
    if data:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({'success': False, 'message': message}), status_code

def created_response(message, data=None):
    return success_response(message, data, 201)

def not_found_response(message="Resource not found"):
    return error_response(message, 404)