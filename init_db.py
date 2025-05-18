from budget_tracker.extensions import db
from budget_tracker import create_app
from budget_tracker.models.category_models import Category

def init_database():
    app = create_app()
    with app.app_context():
        if not Category.query.first():
            default_categories = [
                {"name": "Groceries", "icon": "🛒"},
                {"name": "Rent", "icon": "🏠"},
                {"name": "Utilities", "icon": "💡"},
                {"name": "Transport", "icon": "🚌"},
                {"name": "Health", "icon": "💊"},
            ]
            for cat in default_categories:
             db.session.add(Category(name=cat["name"], icon=cat["icon"], is_default=True))
            
            db.session.commit()
            print("✅ Database initialized with default categories.")
        else:
            print("ℹ️ Default categories already exist.")

if __name__ == '__main__':
    init_database()            
