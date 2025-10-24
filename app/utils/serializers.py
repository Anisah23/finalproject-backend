def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'bio': user.bio,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }

def serialize_artwork(artwork):
    return {
        'id': artwork.id,
        'title': artwork.title,
        'description': artwork.description,
        'price': artwork.price,
        'category': artwork.category,
        'image_url': artwork.image_url,
        'is_available': artwork.is_available,
        'created_at': artwork.created_at.isoformat() if artwork.created_at else None,
        'artist_id': artwork.artist_id
    }

def serialize_order(order):
    return {
        'id': order.id,
        'collector_id': order.collector_id,
        'total_amount': order.total_amount,
        'status': order.status,
        'shipping_address': order.shipping_address,
        'created_at': order.created_at.isoformat() if order.created_at else None,
        'items': [serialize_order_item(item) for item in order.items]
    }

def serialize_order_item(order_item):
    return {
        'id': order_item.id,
        'artwork_id': order_item.artwork_id,
        'price': order_item.price
    }