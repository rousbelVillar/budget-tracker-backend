from datetime import timedelta
import uuid, os
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required, set_access_cookies, unset_jwt_cookies
from budget_tracker.extensions import db
from budget_tracker.auth_utils import  verify_auth_token
from sqlalchemy.exc import IntegrityError
from budget_tracker.models.user_models import User, UserDetails, UserPicture
from functools import wraps
from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from supabase import create_client
from dotenv import load_dotenv


auth_bp = Blueprint("auth", __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
BUCKET_NAME = "photos"

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        file = request.files.get("profile_pic")
        last_name = request.form.get("lastName")
        
        if not name or not email or not password:
            return jsonify({"message": "Missing required fields"}), 400

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)   
        db.session.flush() 
        userDetails = UserDetails(user_id=user.id,name=name,last_name=last_name)
        db.session.add(userDetails)
        if file and allowed_file(file.filename):

            add_image(file,user)
        db.session.commit()

         
    except IntegrityError as e:
        print(e)  
        db.session.rollback()
        return jsonify({"message": "An Error Has Occurred."}), 400
    
    except Exception as e:       
        print(e)   # ← add this
        db.session.rollback()
        print("REGISTRATION ERROR:", type(e).__name__, e)
        return jsonify({"message": str(e)}), 500


    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))

    resp = jsonify(user.serialize())
    set_access_cookies(resp, access_token, max_age=60 * 60 * 24 * 7)
    return resp

def add_image(file,user) :
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    
    # Read file contents
    contents = file.read()
    # Upload to Supabase Storage
    supabase.storage.from_(BUCKET_NAME).upload(unique_name, contents)

    # Get public URL (string)
    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)

    # Insert record into database
    if not user.picture :
        supabase.table(BUCKET_NAME).\
            insert({"title": user.id, "image_url": public_url}).execute()
    # else :
    #     supabase.table(BUCKET_NAME).\
    #         update({})
    
    picture = UserPicture(user_id=user.id, filename=public_url, mimetype=file.mimetype)

    db.session.add(picture)
    return picture


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

@auth_bp.route("/profile/update",methods=["POST"])
@jwt_required()
def profile_update():
    print("Updating profile",request.form)
    return jsonify({})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS