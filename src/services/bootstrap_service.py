from src.extensions import bcrypt, db
from src.models import Admin


def initialize_database() -> None:
    db.create_all()
    ensure_default_admin()


def ensure_default_admin() -> None:
    if Admin.query.filter_by(username="admin").first():
        return

    hashed_password = bcrypt.generate_password_hash("admin123").decode("utf-8")
    admin = Admin(username="admin", password_hash=hashed_password)
    db.session.add(admin)
    db.session.commit()
