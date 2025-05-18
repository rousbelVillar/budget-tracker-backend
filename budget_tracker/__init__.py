#__init__.py
from flask import Flask
from .routes.transaction_routes import transaction_bp
from .routes.category_routes import category_bp
from flask_cors import CORS
from budget_tracker.extensions import db

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///budget.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["TESTING"] = False


    CORS(app,resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(category_bp, url_prefix='/categories')

    with app.app_context():
        db.create_all()

    return app


