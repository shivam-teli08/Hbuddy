from src.extensions import bcrypt, db
from src.models import Business, BusinessUser


def get_all_businesses():
    return Business.query.order_by(Business.created_at.desc()).all()


def register_business(name: str, username: str, password: str, business_type: str | None = None):
    business = Business(name=name, business_type=business_type or "Restaurant")
    db.session.add(business)
    db.session.flush()

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = BusinessUser(
        business_id=business.id,
        username=username,
        password_hash=hashed_password,
    )
    db.session.add(user)
    db.session.commit()
    return business
