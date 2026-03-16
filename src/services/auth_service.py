from flask_login import current_user

from src.extensions import bcrypt, login_manager
from src.models import Admin, BusinessUser


@login_manager.user_loader
def load_user(user_id: str):
    user = BusinessUser.query.get(int(user_id))
    if user:
        return user
    return Admin.query.get(int(user_id))


def authenticate_admin(username: str, password: str):
    admin = Admin.query.filter_by(username=username).first()
    if admin and bcrypt.check_password_hash(admin.password_hash, password):
        return admin
    return None


def authenticate_business_user(username: str, password: str):
    user = BusinessUser.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None


def is_admin_user() -> bool:
    return isinstance(current_user._get_current_object(), Admin)


def is_business_user() -> bool:
    return isinstance(current_user._get_current_object(), BusinessUser)
