def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }

def serialize_artwork(artwork):
    return {
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'image_url': artwork.image_url,
        'is_available': artwork.is_available,
        'artist_id': artwork.artist_id
    }

def serialize_order(order):
    return {
        'id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat() if order.created_at else None
    }