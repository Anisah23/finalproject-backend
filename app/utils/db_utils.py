from app.models import db

def commit():
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def get_or_404(model, id):
    return model.query.get_or_404(id)