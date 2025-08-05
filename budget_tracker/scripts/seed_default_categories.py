from budget_tracker.models.category_models import Category
from budget_tracker.extensions import db
from budget_tracker.models.user_models import User
from budget_tracker.scripts.seed_default_user import create_default_user


def create_default_categories():
    if not Category.query.first():
                default_user = create_default_user()
                print(default_user)
                default_categories = [
                    {"name": "Groceries", "icon": "🛒","user_id":default_user.id},
                    {"name": "Rent", "icon": "🏠","user_id":default_user.id},
                    {"name": "Utilities", "icon": "💡","user_id":default_user.id},
                    {"name": "Transport", "icon": "🚌","user_id":default_user.id},
                    {"name": "Health", "icon": "💊","user_id":default_user.id},
                ]
                for cat in default_categories:
                    db.session.add(Category(name=cat["name"], icon=cat["icon"],user_id=cat["user_id"], is_default=True))
                
                db.session.commit()
                print("✅ Database initialized with default categories.")
    else:
        print("ℹ️ Default categories already exist.")
