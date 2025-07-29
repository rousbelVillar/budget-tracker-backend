#__init__.py
import os
from flask import Flask

from budget_tracker.routes import auth_routes
from .routes.transaction_routes import transaction_bp
from flask_cors import CORS

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["TESTING"] = True
        print("testing config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///budget.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["TESTING"] = False


    CORS(app,resources={r"/*": {"origins": "*"}})
    CORS(app, supports_credentials=True)
    db.init_app(app)

    

    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(auth_routes)
    app.secret_key = os.environ.get("SECRET_KEY") or "super-secret"
    app.config['SESSION_TYPE'] = 'filesystem'

    with app.app_context():
        db.create_all()

    return app


