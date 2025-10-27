from flask import Blueprint, request, jsonify
from app.models import Artwork, User
from app import db
from flask_jwt_extended import get_jwt_identity
from app.utils.auth_utils import artist_required

artist_bp = Blueprint('artist', __name__)


@artist_bp.route('/upload', methods=['POST'])
@artist_required
def upload_art():
    user = get_jwt_identity()
    data = request.get_json()
    art = Artwork(
        title=data.get('title'),
        description=data.get('description'),
        price=data.get('price'),
        image_urls=[data.get('image_url')] if data.get('image_url') else [],
        artist_id=user['id']
    )
    db.session.add(art)
    db.session.commit()
    return jsonify({'message': 'Art uploaded successfully', 'art_id': art.id}), 201


@artist_bp.route('/<int:art_id>', methods=['PUT'])
@artist_required
def edit_art(art_id):
    user = get_jwt_identity()
    art = Artwork.query.get_or_404(art_id)

    if art.artist_id != user['id']:
        return jsonify({'message': 'You can only edit your own art'}), 403

    data = request.get_json()
    art.title = data.get('title', art.title)
    art.description = data.get('description', art.description)
    art.price = data.get('price', art.price)
    if data.get('image_url'):
        art.image_urls = [data.get('image_url')]

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

@artist_bp.route('/artworks', methods=['GET'])
@artist_required
def get_artist_artworks():
    """Get all artworks for the current artist with pagination"""
    user = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Artwork.query.filter_by(artist_id=user['user_id']).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'artworks': [art.to_dict() for art in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })
