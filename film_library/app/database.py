from app.models import Director
from app.extensions import db


def seed_database():
    """Ensures the presence of an 'unknown' director."""
    if not Director.query.filter_by(name="unknown").first():
        db.session.add(Director(name="unknown"))
        db.session.commit()
