from budget_tracker.extensions import db
from budget_tracker.models.user_models import User

def create_default_user():
    default_user = User.query.filter_by(email="default@system").first()
    if not default_user:
        default_user = User(
            email="default@system",
            name="defaultUser",  
        )
        default_user.set_password("sTewug-qlD5l")
        db.session.add(default_user)
        db.session.commit()
    return default_user
