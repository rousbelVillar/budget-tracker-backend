from budget_tracker import create_app
from budget_tracker.scripts.seed_default_categories import create_default_categories

def init_database():
    app = create_app()
    with app.app_context():
        create_default_categories()
        
       
if __name__ == '__main__':
    init_database()            
