from flask import Blueprint

from src.controllers.admin_controller import dashboard, register_business_view


admin_blueprint = Blueprint("admin", __name__)

admin_blueprint.get("/dashboard")(dashboard)
admin_blueprint.route("/register_business", methods=["GET", "POST"])(register_business_view)
