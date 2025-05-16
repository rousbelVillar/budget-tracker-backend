from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes.transaction_routes import transaction_bp
from .routes.category_routes import category_bp
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == "testing":
        app.config.from_object("budget_tracker.config.TestConfig")
    else:
        app.config.from_object("budget_tracker.config.Config")

    CORS(app)
    db.init_app(app)

    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(category_bp, url_prefix='/categories')

    return app
