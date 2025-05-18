from budget_tracker import create_app;
from budget_tracker.models.category_models import db,Category
from sqlalchemy import select, delete


app = create_app()

def display_categories():
    print(db.session.execute(select(Category.name,Category.id,Category.is_default)).all())
def delete_category():
    c = Category.query.get(7)
    db.session.delete(c)
    db.session.commit()
    print("Category deleted.")

with app.app_context():
    display_categories()
    
