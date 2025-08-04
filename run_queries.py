from budget_tracker import create_app;
from budget_tracker.models.category_models import db,Category
from budget_tracker.models.transaction_models import Transaction

from sqlalchemy import select, delete

from budget_tracker.models.user_models import User


app = create_app()

def display_categories():
    print(db.session.execute(select(Category.name,Category.id,Category.is_default)).all().__format__())
def display_transactions():
    print(db.session.execute(select(Transaction.amount,Transaction.category,Transaction.date,Transaction.description,Transaction.id)).all())
def delete_category():
    c = Category.query.get(7)
    db.session.delete(c)
    db.session.commit()
def display_users():
    print(db.session.execute(select(User.name,User.password_hash)).all())
def delete_user():
    stmt = delete(User).where(User.name == "test")
    db.session.execute(stmt)
    db.session.commit()   
    print(db.session.execute(select(User).where(User.name=="test")).first())

with app.app_context():
     delete_user()
    
