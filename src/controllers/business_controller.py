from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from src.services.billing_service import build_bill_pdf, generate_bill_number
from src.services.auth_service import is_business_user
from src.services.business_service import (
    add_category,
    add_menu_item,
    add_table,
    complete_business_setup,
    get_business_categories,
    get_business_tables,
    get_dashboard_metrics,
    get_order_history,
    get_order_for_business,
    get_table_for_business,
    mark_order_completed,
    toggle_menu_item_availability,
    update_table_status,
)
from src.services.order_service import create_order_for_table


def _guard_business_user():
    if not is_business_user():
        return redirect(url_for("auth.admin_login"))
    return None


@login_required
def setup():
    guard = _guard_business_user()
    if guard:
        return guard

    if request.method == "POST":
        complete_business_setup(current_user, request.form)
        flash("Setup completed successfully")
        return redirect(url_for("business.dashboard"))
    return render_template("business/setup.html")


@login_required
def dashboard():
    guard = _guard_business_user()
    if guard:
        return guard
    if not current_user.is_setup_completed:
        return redirect(url_for("business.setup"))

    metrics = get_dashboard_metrics(current_user.business_id)
    return render_template("business/dashboard.html", **metrics)


@login_required
def menu_management():
    guard = _guard_business_user()
    if guard:
        return guard

    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_category":
            add_category(current_user.business_id, request.form.get("name"))
            flash("Category added successfully")
        elif action == "add_item":
            add_menu_item(
                current_user.business_id,
                int(request.form.get("category_id")),
                request.form.get("name"),
                float(request.form.get("price")),
            )
            flash("Menu item added successfully")
        elif action == "toggle_item":
            toggle_menu_item_availability(
                current_user.business_id,
                int(request.form.get("item_id")),
            )
            flash("Menu item availability updated")
        return redirect(url_for("business.menu_management"))

    categories = get_business_categories(current_user.business_id)
    return render_template("business/menu.html", categories=categories)


@login_required
def table_management():
    guard = _guard_business_user()
    if guard:
        return guard

    if request.method == "POST":
        action = request.form.get("action", "add")
        if action == "add":
            add_table(
                current_user.business_id,
                request.form.get("name"),
                int(request.form.get("capacity")),
            )
            flash("Table added successfully")
        elif action == "status":
            update_table_status(
                current_user.business_id,
                int(request.form.get("table_id")),
                request.form.get("status"),
            )
            flash("Table status updated")
        return redirect(url_for("business.table_management"))

    tables = get_business_tables(current_user.business_id)
    return render_template("business/table_map.html", tables=tables)


@login_required
def create_order(table_id: int):
    guard = _guard_business_user()
    if guard:
        return guard

    table = get_table_for_business(table_id, current_user.business_id)

    if request.method == "POST":
        order = create_order_for_table(
            current_user.business_id,
            table.id,
            request.form.getlist("items"),
            request.form.getlist("quantities"),
        )
        flash("Order placed successfully")
        return redirect(url_for("business.view_bill", order_id=order.id))

    categories = get_business_categories(current_user.business_id)
    return render_template("business/order.html", table=table, categories=categories)


@login_required
def order_history():
    guard = _guard_business_user()
    if guard:
        return guard

    orders = get_order_history(current_user.business_id)
    return render_template("business/order_history.html", orders=orders)


@login_required
def complete_order(order_id: int):
    guard = _guard_business_user()
    if guard:
        return guard

    mark_order_completed(current_user.business_id, order_id)
    flash("Order marked as paid and completed")
    return redirect(url_for("business.order_history"))


@login_required
def view_bill(order_id: int):
    guard = _guard_business_user()
    if guard:
        return guard

    order = get_order_for_business(current_user.business_id, order_id)
    return render_template(
        "business/bill.html",
        order=order,
        bill_number=generate_bill_number(order),
    )


@login_required
def download_bill_pdf(order_id: int):
    guard = _guard_business_user()
    if guard:
        return guard

    order = get_order_for_business(current_user.business_id, order_id)
    pdf_buffer = build_bill_pdf(order)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{generate_bill_number(order)}.pdf",
        mimetype="application/pdf",
    )
