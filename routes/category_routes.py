from flask import request, jsonify
from flask import Blueprint
from models.transaction_models import Category, db

routes_bp = Blueprint('routes_categories', __name__)


@routes_bp.before_app_request
def seed_default_categories():
    default_categories = [
        {"name": "Groceries", "icon": "🛒"},
        {"name": "Rent", "icon": "🏠"},
        {"name": "Utilities", "icon": "💡"},
        {"name": "Transport", "icon": "🚌"},
        {"name": "Health", "icon": "💊"},
    ]
    for cat in default_categories:
        exists = Category.query.filter_by(name=cat["name"]).first()
        if not exists:
            db.session.add(Category(name=cat["name"], icon=cat["icon"], is_default=True))
    db.session.commit()


@routes_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "icon": c.icon,
        "is_default": c.is_default
    } for c in categories])

@routes_bp.route("/categories", methods=["POST"])
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
