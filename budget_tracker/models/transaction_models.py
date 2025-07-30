from sqlalchemy import DateTime
from datetime import datetime
from budget_tracker.extensions import db
import pytz

class Transaction(db.Model):
    tz_ny = pytz.timezone('America/Los_Angeles')
    now_la = datetime.now(tz_ny)
    print('now_la',now_la)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(DateTime, default=now_la)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
