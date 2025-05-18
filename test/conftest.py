import pytest
from budget_tracker.extensions import db

@pytest.fixture
def client():
    app = db('testing')  

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
