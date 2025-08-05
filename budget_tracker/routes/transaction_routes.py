#transactions_routes.py

from flask import request, jsonify
from ..models.transaction_models import db, Transaction
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity


transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/add', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.json.get("params")
    t = Transaction(
        type=data['type'],
        amount=data['amount'],
        category=data['category'],
        description=data['description'],
        user_id=user_id
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'id': t.id}), 201

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    transaction.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@transaction_bp.route('/get', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_transactions():
    if request.method == "OPTIONS":
        return '', 200
    user_id = get_jwt_identity()
    month = request.args.get('month')  # e.g.,'2025-05'
    transactions = Transaction.query.filter_by(user_id=user_id,is_deleted=False).order_by(Transaction.date.desc()).all()
    if month and len(transactions) > 0:
        query = query.filter(Transaction.date.startswith(month))
    elif len(transactions) > 0:
        transactions = transactions
    return jsonify([{
        'id': t.id,
        'date': t.date,
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'description': t.description
    } for t in transactions])