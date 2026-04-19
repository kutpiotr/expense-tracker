import os
from flask import Flask
from app.extensions import db, migrate, cors
from app.config import Config
from app.errors import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    register_error_handlers(app)

    # Upewnij się, że folder instance/ istnieje
    os.makedirs(app.instance_path, exist_ok=True)

    # Rozszerzenia
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    from app import models  # noqa: F401
    from app.api.transactions import bp as transactions_bp
    from app.api.categories import bp as categories_bp

    app.register_blueprint(transactions_bp)
    app.register_blueprint(categories_bp)

    @app.route("/")
    def index():
        return {"status": "ok", "service": "expense-tracker-api"}

    return app
