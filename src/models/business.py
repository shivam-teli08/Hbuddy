from src.extensions import db
from src.models.base import TimestampMixin


class Business(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    contact = db.Column(db.String(20))
    gst_number = db.Column(db.String(20))
    business_type = db.Column(db.String(50))
    opening_time = db.Column(db.String(10))
    closing_time = db.Column(db.String(10))
    working_days = db.Column(db.String(100))
    subscription_status = db.Column(db.String(20), default="Active", nullable=False)
