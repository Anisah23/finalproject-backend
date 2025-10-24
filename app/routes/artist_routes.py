from flask import Blueprint, request, jsonify
from app.models import Art, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

artist_bp = Blueprint('artist', __name__)

def artist_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if user['role'] != 'artist':
            return jsonify({'message': 'Only artists can perform this action'}), 403
        return fn(*args, **kwargs)
    return wrapper


@artist_bp.route('/upload', methods=['POST'])
@artist_required
def upload_art():
    user = get_jwt_identity()
    data = request.get_json()
    art = Art(
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price'),
        image_url=data.get('image_url'),
        artist_id=user['id']
    )
    db.session.add(art)
    db.session.commit()
    return jsonify({'message': 'Art uploaded successfully', 'art_id': art.id}), 201


@artist_bp.route('/<int:art_id>', methods=['PUT'])
@artist_required
def edit_art(art_id):
    user = get_jwt_identity()
    art = Art.query.get_or_404(art_id)

    if art.artist_id != user['id']:
        return jsonify({'message': 'You can only edit your own art'}), 403

    data = request.get_json()
    art.title = data.get('title', art.title)
    art.description = data.get('description', art.description)
    art.price = data.get('price', art.price)
    art.image_url = data.get('image_url', art.image_url)

    db.session.commit()
    return jsonify({'message': 'Art updated successfully'})


@artist_bp.route('/<int:art_id>', methods=['DELETE'])
@artist_required
def delete_art(art_id):
    user = get_jwt_identity()
    art = Art.query.get_or_404(art_id)

    if art.artist_id != user['id']:
        return jsonify({'message': 'You can only delete your own art'}), 403

    db.session.delete(art)
    db.session.commit()
    return jsonify({'message': 'Art deleted successfully'})
