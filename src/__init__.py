from flask import Flask

from src.config import Config
from src.extensions import bcrypt, db, login_manager
from src.routes.admin_routes import admin_blueprint
from src.routes.auth_routes import auth_blueprint
from src.routes.business_routes import business_blueprint
from src.routes.legacy_routes import legacy_blueprint


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(business_blueprint, url_prefix="/business")
    app.register_blueprint(legacy_blueprint)

    return app
