from flask import abort

from src.extensions import db
from src.models import MenuItem, Order, OrderItem
from src.services.business_service import get_table_for_business


def create_order_for_table(business_id: int, table_id: int, item_ids: list[str], quantities: list[str]):
    table = get_table_for_business(table_id, business_id)

    order = Order(business_id=business_id, table_id=table.id)
    db.session.add(order)
    db.session.flush()

    total = 0.0
    for item_id, qty in zip(item_ids, quantities):
        quantity = int(qty)
        if quantity <= 0:
            continue
        item = MenuItem.query.filter_by(id=int(item_id), business_id=business_id).first()
        if item is None:
            abort(404)
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.id,
            quantity=quantity,
            price_at_order=item.price,
        )
        db.session.add(order_item)
        total += item.price * quantity

    order.total_amount = total
    order.gst_amount = round(total * 0.05, 2)
    order.final_amount = round(order.total_amount + order.gst_amount, 2)
    table.status = "Occupied"
    db.session.commit()
    return order
