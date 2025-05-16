from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
import pytz

db = SQLAlchemy()

class Transaction(db.Model):
    tz_ny = pytz.timezone('America/Los_Angeles')
    now_la = datetime.now(tz_ny)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(DateTime, default=now_la)     # YYYY-MM-DD HH:MM:SS TZ
    type = db.Column(db.String(10), nullable=False)     # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    icon = db.Column(db.String, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
