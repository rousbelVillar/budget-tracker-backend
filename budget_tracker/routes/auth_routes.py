from datetime import timedelta
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from budget_tracker.extensions import db
from budget_tracker.auth_utils import generate_auth_token, verify_auth_token
from sqlalchemy.exc import IntegrityError
from budget_tracker.models.user_models import User
from functools import wraps
from flask import request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User(name=name, email=email)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already registered"}), 400

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
    resp = make_response(user.serialize())
    set_access_cookies(resp, access_token, max_age=60 * 60 * 24 * 7)
    return resp


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
    
    response = jsonify(user.serialize())
    set_access_cookies(response, access_token, max_age=60 * 60 * 24 * 7)

    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"message": "Logged out"})
    unset_jwt_cookies(resp)
    return resp



@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize())


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
