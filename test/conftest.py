import pytest
from budget_tracker import create_app, db

@pytest.fixture
def client():
    app = create_app('testing')  

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
