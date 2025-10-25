def user_dict(user):
    return {
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role
    }

def artwork_dict(artwork):
    return {
        'id': artwork.id,
        'title': artwork.title,
        'price': artwork.price,
        'image_url': artwork.image_url,
        'artist_id': artwork.artist_id
    }