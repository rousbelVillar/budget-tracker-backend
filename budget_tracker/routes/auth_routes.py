from datetime import timedelta
import uuid, os
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from budget_tracker.extensions import db
from budget_tracker.auth_utils import generate_auth_token, verify_auth_token
from sqlalchemy.exc import IntegrityError
from budget_tracker.models.user_models import User, UserPicture
from functools import wraps
from flask import request, jsonify, make_response, send_from_directory, current_app, Blueprint
from werkzeug.utils import secure_filename
from supabase import create_client,Client
from dotenv import load_dotenv



auth_bp = Blueprint("auth", __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
BUCKET_NAME = "photos"

@auth_bp.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    file = request.files.get("profile_pic")

    if not name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    picture = None

    # Load environment variables
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase = create_client(url, key)


    try:
        db.session.add(user)
        db.session.flush() 
        if file and allowed_file(file.filename):
            ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            # Read file contents
            contents = file.read()
            # Upload to Supabase Storage
            supabase.storage.from_(BUCKET_NAME).upload(unique_name, contents)

            # Get public URL (string)
            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)

            # Insert record into database
            supabase.table(BUCKET_NAME).\
                insert({"title": user.id, "image_url": public_url}).execute()
            
            picture = UserPicture(user_id=user.id, filename=public_url, mimetype=file.mimetype)
            print('picture',picture)
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
    profile_pic = UserPicture.query.get(user_id)
    if not profile_pic:
        return jsonify(user.serialize())
    return jsonify({
        "email": user.email,
        "id": user.id,
        "name":user.name,
        "profile_image_url":profile_pic.filename
    })

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS