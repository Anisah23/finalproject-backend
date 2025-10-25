from flask import jsonify

def success(message, data=None):
    response = {'message': message}
    if data:
        response['data'] = data
    return jsonify(response), 200

def error(message, code=400):
    return jsonify({'message': message}), code

def created(message, data=None):
    return success(message, data), 201