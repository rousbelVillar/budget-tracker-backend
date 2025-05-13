from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    icon = db.Column(db.String, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
