# __init__.py

from flask import Flask
from .routes.transaction_routes import transaction_bp
from .routes.category_routes import category_bp
from .routes.auth_routes import auth_bp
from flask_cors import CORS
from budget_tracker.extensions import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Database setup
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["TESTING"] = False

    # JWT setup
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # Set to True in production (requires HTTPS)
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-CSRF-TOKEN"
    app.config["JWT_CSRF_METHODS"] = ["POST", "PUT", "PATCH", "DELETE"]

    # CORS setup
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173"],
        allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # Register extensions and blueprints
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app
