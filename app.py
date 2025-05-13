from flask import Flask
from flask_cors import CORS
from models.transaction_models import db
from routes.transaction_routes import routes_bp as transaction_blueprint
from routes.category_routes import routes_bp as category_blueprint


app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(transaction_blueprint)
app.register_blueprint(category_blueprint)

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
