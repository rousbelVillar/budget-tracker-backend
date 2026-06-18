from functools import wraps
from flask import jsonify, request
from budget_tracker.auth_utils import verify_auth_token

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"message": "Not authenticated"}), 401
        user_id = verify_auth_token(token)
        if not user_id:
            return jsonify({"message": "Invalid or expired session"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated_function