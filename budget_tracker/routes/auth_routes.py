from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required, set_access_cookies, unset_jwt_cookies
from budget_tracker.extensions import db
from sqlalchemy.exc import IntegrityError
from budget_tracker.models.user_models import User, UserDetails, UserPicture
from budget_tracker.modules.user_module import User as UserModule
from flask import request, jsonify, Blueprint


auth_bp = Blueprint("auth", __name__)

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
        user_details = UserDetails(user_id=user.id,name=name,last_name=last_name)
        db.session.add(user_details)
        user_module = UserModule()

        if file and user_module.allowed_file(file.filename):
            user_module.add_image(file,user)      
            picture = UserPicture(user_id=user.id, filename=user_module.public_url, mimetype=file.mimetype)
            db.session.add(picture)
        db.session.commit()

         
    except IntegrityError as e:
        print(e)  
        db.session.rollback()
        return jsonify({"message": "An Error Has Occurred."}), 400
    
    except Exception as e:       
        print(e)
        db.session.rollback()
        print("REGISTRATION ERROR:", type(e).__name__, e)
        return jsonify({"message": str(e)}), 500


    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))

    resp = jsonify(user.serialize())
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

@auth_bp.route("/profile/update",methods=["POST"])
@jwt_required()
def profile_update():

    try:
        user_id = get_jwt_identity()
        name = request.form.get("name")
        last_name = request.form.get("lastName")
        #password = request.form.get("password")
        file = request.files.get('profile_pic') 
        if not user_id:
            return jsonify({"message": "Invalid credentials"}), 401
        else:
            user = User.query.get(user_id)
            user_details = UserDetails.query.get(user_id)
            user_picture = UserPicture.query.get(user_id)
            if name:
                user_details.name = name
            if last_name:
                user_details.last_name = last_name
            user_module = UserModule()
            if file and user_module.allowed_file(file.filename):
                user_module.add_image(file,user) 
                user_picture.filename = user_module.public_url   
                user_picture.mimetype = file.mimetype
        
    except Exception as e:       
        print(e)
        db.session.rollback()
        print("REGISTRATION ERROR:", type(e).__name__, e)
        return jsonify({"message": str(e)}), 500
    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.serialize()}), 200
