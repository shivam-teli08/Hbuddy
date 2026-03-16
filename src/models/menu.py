from src.extensions import db


class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    business = db.relationship("Business", backref=db.backref("categories", lazy=True))


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("menu_category.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))

    category = db.relationship("MenuCategory", backref=db.backref("items", lazy=True))
