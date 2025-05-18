#category_routes.py
from flask import request, jsonify
from flask import Blueprint
from ..models.category_models import Category, db

category_bp = Blueprint('categories', __name__)


@category_bp.route("/add", methods=["POST"])
def add_category():
    data = request.json
    name = data.get("name")
    icon = data.get("icon", "📝")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    exists = Category.query.filter_by(name=name).first()
    if exists:
        return jsonify({"error": "Category already exists"}), 400
    category = Category(name=name, icon=icon, is_default=False)
    db.session.add(category)
    db.session.commit()
    return jsonify({
        "id": category.id,
        "name": category.name,
        "icon": category.icon,
        "is_default": category.is_default
    }), 201

@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "icon": c.icon,
        "is_default": c.is_default
    } for c in categories])
