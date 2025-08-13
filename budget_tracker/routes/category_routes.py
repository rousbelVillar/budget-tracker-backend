#category_routes.py
from flask import request, jsonify
from flask import Blueprint
from budget_tracker.models.user_models import User
from ..models.category_models import Category, db
from flask_jwt_extended import jwt_required, get_jwt_identity


category_bp = Blueprint('categories', __name__)


@category_bp.route("/add", methods=["POST"])
@jwt_required()
def add_category():
    data = request.json.get("params")
    name = data.get("name")
    icon = data.get("icon", "📝")
    user_id = get_jwt_identity()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    exists = Category.query.filter_by(name=name,user_id=user_id).first()
    if exists:
        return jsonify({"error": "Category already exists"}), 400
    category = Category(name=name, icon=icon, is_default=False,user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return jsonify({
        "id": category.id,
        "name": category.name,
        "icon": category.icon,
        "is_default": category.is_default
    }), 201

@category_bp.route("/get", methods=["GET"])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    default_user = User.query.filter_by(email="default@system").first()

    categories = Category.query.filter(
        Category.user_id.in_([user.id, default_user.id])
    ).all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "icon": c.icon,
        "is_default": c.is_default
    } for c in categories])

@category_bp.route("/add/bulk",methods=["POST"])
@jwt_required()
def add_categories_bulk():
    user_id = get_jwt_identity()
    categories_data = request.get_json()


    if not isinstance(categories_data,list):
        return jsonify({"error": "Expected a list of categories"}), 400
    categories = []
    for entry in categories_data:
        try:
            category = Category(
                name= entry["name"],
                is_default= entry["is_default"],
                user_id=user_id,
                icon=entry["icon"]
            )
        except KeyError as e:
            return jsonify({"error": f"Missing field {str(e)}"}), 400
        categories.append(category)
    db.session.add_all(categories)
    db.session.commit()

    return jsonify({"message": f"{len(categories)} transactions added"}), 201