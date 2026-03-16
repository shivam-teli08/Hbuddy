from flask import Blueprint

from src.controllers.auth_controller import admin_login, login, logout


auth_blueprint = Blueprint("auth", __name__)

auth_blueprint.route("/login", methods=["GET", "POST"])(login)
auth_blueprint.route("/business/login", methods=["GET", "POST"])(login)
auth_blueprint.route("/admin/login", methods=["GET", "POST"])(admin_login)
auth_blueprint.get("/logout")(logout)
