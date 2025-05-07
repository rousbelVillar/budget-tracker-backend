from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)     # YYYY-MM-DD
    type = db.Column(db.String(10), nullable=False)     # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
