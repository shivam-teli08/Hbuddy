from src.extensions import db
from src.models.base import TimestampMixin


class Order(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("restaurant_table.id"), nullable=False)
    status = db.Column(db.String(20), default="Active")
    payment_status = db.Column(db.String(20), default="Pending")
    total_amount = db.Column(db.Float, default=0.0)
    gst_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)

    table = db.relationship("RestaurantTable", backref=db.backref("orders", lazy=True))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_at_order = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", backref=db.backref("items", lazy=True))
    menu_item = db.relationship("MenuItem")
