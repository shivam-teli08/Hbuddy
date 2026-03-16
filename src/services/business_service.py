from datetime import datetime

from flask import abort

from src.extensions import db
from src.models import Business, MenuCategory, MenuItem, Order, RestaurantTable


def complete_business_setup(user, form_data):
    business = user.business
    business.address = form_data.get("address")
    business.contact = form_data.get("contact")
    business.gst_number = form_data.get("gst_number")
    business.business_type = form_data.get("business_type")
    business.opening_time = form_data.get("opening_time")
    business.closing_time = form_data.get("closing_time")
    business.working_days = form_data.get("working_days")
    user.is_setup_completed = True
    db.session.commit()


def get_dashboard_metrics(business_id: int):
    today = datetime.utcnow().date()
    orders = Order.query.filter(
        Order.business_id == business_id,
        db.func.date(Order.created_at) == today,
    ).all()
    total_revenue = sum(order.final_amount for order in orders if order.status == "Completed")
    active_tables = RestaurantTable.query.filter_by(
        business_id=business_id,
        status="Occupied",
    ).count()
    completed_orders = len([order for order in orders if order.status == "Completed"])
    return {
        "orders_count": len(orders),
        "total_revenue": total_revenue,
        "active_tables": active_tables,
        "completed_orders": completed_orders,
        "recent_orders": Order.query.filter_by(business_id=business_id)
        .order_by(Order.created_at.desc())
        .limit(8)
        .all(),
    }


def get_business_categories(business_id: int):
    return MenuCategory.query.filter_by(business_id=business_id).order_by(MenuCategory.name.asc()).all()


def add_category(business_id: int, name: str):
    category = MenuCategory(business_id=business_id, name=name)
    db.session.add(category)
    db.session.commit()


def add_menu_item(business_id: int, category_id: int, name: str, price: float):
    item = MenuItem(
        business_id=business_id,
        category_id=category_id,
        name=name,
        price=price,
    )
    db.session.add(item)
    db.session.commit()


def toggle_menu_item_availability(business_id: int, item_id: int):
    item = MenuItem.query.filter_by(id=item_id, business_id=business_id).first()
    if item is None:
        abort(404)
    item.is_available = not item.is_available
    db.session.commit()


def get_business_tables(business_id: int):
    return RestaurantTable.query.filter_by(business_id=business_id).order_by(RestaurantTable.name.asc()).all()


def add_table(business_id: int, name: str, capacity: int):
    table = RestaurantTable(business_id=business_id, name=name, capacity=capacity)
    db.session.add(table)
    db.session.commit()


def update_table_status(business_id: int, table_id: int, status: str):
    table = RestaurantTable.query.filter_by(id=table_id, business_id=business_id).first()
    if table is None:
        abort(404)
    table.status = status
    db.session.commit()
    return table


def get_table_for_business(table_id: int, business_id: int):
    table = RestaurantTable.query.get_or_404(table_id)
    if table.business_id != business_id:
        abort(403)
    return table


def get_order_history(business_id: int):
    return Order.query.filter_by(business_id=business_id).order_by(Order.created_at.desc()).all()


def mark_order_completed(business_id: int, order_id: int):
    order = Order.query.filter_by(id=order_id, business_id=business_id).first()
    if order is None:
        abort(404)
    order.status = "Completed"
    order.payment_status = "Paid"
    order.table.status = "Available"
    db.session.commit()
    return order


def get_order_for_business(business_id: int, order_id: int):
    order = Order.query.filter_by(id=order_id, business_id=business_id).first()
    if order is None:
        abort(404)
    return order
