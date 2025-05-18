from . import db
from datetime import datetime
import pytz


class Transaction(db.Model):
    # Define the UTC-7 timezone
    utc_minus_7_tz = pytz.FixedOffset(-7 * 60)  # Offset in minutes
    # Get current time in UTC-7
    now_utc_minus_7_pytz = datetime.now(utc_minus_7_tz)
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255))
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=now_utc_minus_7_pytz)
