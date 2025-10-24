from flask import Blueprint, request, jsonify
from app.models import Art, Transaction, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

collector_bp = Blueprint('collector', __name__)


def collector_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if user['role'] != 'collector':
            return jsonify({'message': 'Only collectors can perform this action'}), 403
        return fn(*args, **kwargs)
    return wrapper


@collector_bp.route('/browse', methods=['GET'])
@jwt_required()
def browse_arts():
    arts = Art.query.all()
    return jsonify([{
        'id': art.id,
        'title': art.title,
        'description': art.description,
        'price': art.price,
        'image_url': art.image_url,
        'artist_id': art.artist_id
    } for art in arts])


@collector_bp.route('/purchase/<int:art_id>', methods=['POST'])
@collector_required
def purchase_art(art_id):
    user = get_jwt_identity()
    art = Art.query.get_or_404(art_id)

   
    transaction = Transaction(
        art_id=art.id,
        buyer_id=user['id'],
        amount=art.price,
        status='completed'
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': f'You purchased "{art.title}" successfully', 'transaction_id': transaction.id})
