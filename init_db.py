from app import app
from models.transaction_models import db

with app.app_context():
    
    db.create_all()
    print("✅ Tables created successfully.")
