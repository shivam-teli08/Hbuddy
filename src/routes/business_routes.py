from flask import Blueprint

from src.controllers.business_controller import (
    complete_order,
    create_order,
    dashboard,
    download_bill_pdf,
    menu_management,
    order_history,
    setup,
    table_management,
    view_bill,
)


business_blueprint = Blueprint("business", __name__)

business_blueprint.route("/", methods=["GET"])(dashboard)
business_blueprint.route("/dashboard", methods=["GET"])(dashboard)
business_blueprint.route("/setup", methods=["GET", "POST"])(setup)
business_blueprint.route("/menu", methods=["GET", "POST"])(menu_management)
business_blueprint.route("/tables", methods=["GET", "POST"])(table_management)
business_blueprint.route("/order/<int:table_id>", methods=["GET", "POST"])(create_order)
business_blueprint.get("/orders")(order_history)
business_blueprint.post("/orders/<int:order_id>/complete")(complete_order)
business_blueprint.get("/orders/<int:order_id>/bill")(view_bill)
business_blueprint.get("/orders/<int:order_id>/bill/pdf")(download_bill_pdf)
