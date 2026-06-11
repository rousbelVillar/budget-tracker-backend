from budget_tracker.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', back_populates='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', back_populates='user', lazy=True, cascade='all, delete-orphan')
    picture = db.relationship('UserPicture', back_populates='user', uselist=False, cascade='all, delete-orphan')
    details = db.relationship('UserDetails', back_populates='user', uselist=False, cascade='all, delete-orphan')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def serialize(self):
        try:
            return {
                'id': self.id,
                'email': self.email,
                'profileImage': self.picture.filename if self.picture else None,
                'name': self.details.name if self.details else None,
                'lastName': self.details.last_name if self.details else None,
            }
        except Exception as e:
            return {
                'id': self.id,
                'email': self.email,
                'profileImage': None,
                'name': None,
                'lastName': None,
            }
class UserPicture(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    filename = db.Column(db.String(256), nullable=False)   
    mimetype = db.Column(db.String(64), nullable=False)  
    user = db.relationship('User', back_populates='picture')


class UserDetails(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(256), nullable=False)   
    last_name = db.Column(db.String(256), nullable=False)
    user = db.relationship('User', back_populates='details')  