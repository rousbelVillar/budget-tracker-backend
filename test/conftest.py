import pytest
from budget_tracker import create_app
from budget_tracker.extensions import db

@pytest.fixture
def app():
    app = create_app(config_name='testing')  

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    print("⚡ Client fixture used")
    return app.test_client() 
