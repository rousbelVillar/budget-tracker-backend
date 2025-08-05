# budget_tracker/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///budget.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    TESTING = True
