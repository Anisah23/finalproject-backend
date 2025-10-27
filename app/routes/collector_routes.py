from flask import Blueprint, request, jsonify
from app.models import Artwork, Order, User, Category
from app import db
from flask_jwt_extended import jwt_required
from app.utils.auth_utils import collector_required

collector_bp = Blueprint('collector', __name__)


@collector_bp.route('/browse', methods=['GET'])
def browse_arts():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by', 'created_at')  # created_at, price, title
    sort_order = request.args.get('sort_order', 'desc')  # asc, desc

    # Base query with joins for artist and category
    query = Artwork.query.filter_by(is_available=True).join(User, Artwork.artist_id == User.id).join(Category, Artwork.category_id == Category.id, isouter=True)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Artwork.title.ilike(search_term),
                Artwork.description.ilike(search_term),
                Artwork.tags.contains([search])  # Search in tags array
            )
        )

    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Apply price filters
    if min_price is not None:
        query = query.filter(Artwork.price >= min_price)
    if max_price is not None:
        query = query.filter(Artwork.price <= max_price)

    # Apply sorting
    if sort_by == 'price':
        order_column = Artwork.price
    elif sort_by == 'title':
        order_column = Artwork.title
    else:  # created_at
        order_column = Artwork.created_at

    if sort_order == 'asc':
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    # Apply pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    artworks = pagination.items

    return jsonify({
        'artworks': [{
            'id': art.id,
            'title': art.title,
            'description': art.description,
            'price': float(art.price),
            'currency': art.currency,
            'image_urls': art.image_urls or [],
            'artist_id': art.artist_id,
            'artist': art.artist.full_name,
            'category_id': art.category_id,
            'category': art.category_rel.name if art.category_rel else None,
            'dimensions': art.dimensions,
            'medium': art.medium,
            'year_created': art.year_created,
            'is_featured': art.is_featured,
            'tags': art.tags or [],
            'created_at': art.created_at.isoformat() if art.created_at else None
        } for art in artworks],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
            'next_page': pagination.next_num if pagination.has_next else None,
            'prev_page': pagination.prev_num if pagination.has_prev else None
        }
    })


@collector_bp.route('/purchase/<int:art_id>', methods=['POST'])
@collector_required
def purchase_art(art_id):
    user = get_jwt_identity()
    art = Artwork.query.get_or_404(art_id)

    # Create order
    order = Order(
        buyer_id=user['id'],
        total_amount=art.price,
        status='pending'
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': f'You purchased "{art.title}" successfully', 'order_id': order.id})
