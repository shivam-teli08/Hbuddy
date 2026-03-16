from flask import Blueprint, redirect, url_for


legacy_blueprint = Blueprint("legacy", __name__)


@legacy_blueprint.get("/")
def root_redirect():
    return redirect(url_for("business.dashboard"))


@legacy_blueprint.get("/dashboard")
def dashboard_redirect():
    return redirect(url_for("business.dashboard"))


@legacy_blueprint.route("/setup", methods=["GET", "POST"])
def setup_redirect():
    return redirect(url_for("business.setup"))


@legacy_blueprint.route("/menu", methods=["GET", "POST"])
def menu_redirect():
    return redirect(url_for("business.menu_management"))


@legacy_blueprint.route("/tables", methods=["GET", "POST"])
def tables_redirect():
    return redirect(url_for("business.table_management"))


@legacy_blueprint.route("/order/<int:table_id>", methods=["GET", "POST"])
def order_redirect(table_id: int):
    return redirect(url_for("business.create_order", table_id=table_id))


@legacy_blueprint.get("/orders")
def orders_redirect():
    return redirect(url_for("business.order_history"))


@legacy_blueprint.post("/orders/<int:order_id>/complete")
def complete_order_redirect(order_id: int):
    return redirect(url_for("business.complete_order", order_id=order_id), code=307)


@legacy_blueprint.get("/orders/<int:order_id>/bill")
def bill_redirect(order_id: int):
    return redirect(url_for("business.view_bill", order_id=order_id))


@legacy_blueprint.get("/orders/<int:order_id>/bill/pdf")
def bill_pdf_redirect(order_id: int):
    return redirect(url_for("business.download_bill_pdf", order_id=order_id))
