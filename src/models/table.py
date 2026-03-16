from src.extensions import db


class RestaurantTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, default=4)
    status = db.Column(db.String(20), default="Available")

    business = db.relationship("Business", backref=db.backref("tables", lazy=True))
