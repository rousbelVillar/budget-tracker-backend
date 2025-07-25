from flask import current_app
from itsdangerous import BadSignature, URLSafeTimedSerializer


serializer = URLSafeTimedSerializer("super-secret-key")

def generate_auth_token(user_id):
    return serializer.dumps(user_id, salt="auth")
def verify_auth_token(token):
    try:
        return serializer.loads(token, salt="auth", max_age=3600 * 24 * 7)
    except BadSignature:
        return None