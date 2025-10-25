from app.models import db
from flask import jsonify

def safe_commit():
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False



def get_or_404(model, id):
    return model.query.get_or_404(id)

def paginate_query(query, page=1, per_page=20):
    return query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )