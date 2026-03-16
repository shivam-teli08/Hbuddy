from flask_login import UserMixin

from src.extensions import db


class BusinessUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_setup_completed = db.Column(db.Boolean, default=False)

    business = db.relationship("Business", backref=db.backref("users", lazy=True))
