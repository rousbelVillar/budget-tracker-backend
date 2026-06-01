from datetime import timedelta
import uuid, os
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from budget_tracker.extensions import db
from budget_tracker.auth_utils import generate_auth_token, verify_auth_token
from sqlalchemy.exc import IntegrityError
from budget_tracker.models.user_models import User, UserPicture
from functools import wraps
from flask import request, jsonify
from flask import request, jsonify, make_response, send_from_directory, current_app
from werkzeug.utils import secure_filename

auth_bp = Blueprint("auth", __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


@auth_bp.route("/register", methods=["POST"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    file = request.files.get("profile_pic")   # optional

    if not name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User(name=name, email=email)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.flush()   # gives user.id without committing yet

        if file and allowed_file(file.filename):
            ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
            file.save(save_path)

            picture = UserPicture(user_id=user.id, filename=unique_name, mimetype=file.mimetype)
            db.session.add(picture)

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

@auth_bp.route("/users/<int:user_id>/picture", methods=["GET"])
def get_profile_picture(user_id):
    picture = UserPicture.query.filter_by(user_id=user_id).first_or_404()
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        picture.filename,
        mimetype=picture.mimetype
    )


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
