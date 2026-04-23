#transactions_routes.py

from datetime import datetime

from flask import request, jsonify
from ..models.transaction_models import db, Transaction
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.orm import Session


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
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')  
    max_amount = request.args.get('max_amount')  

    filters = [
        Transaction.is_deleted == False,
        Transaction.user_id == user_id
    ]

    if start_date is not None and end_date is not None:
        start = datetime.strptime(start_date,"%Y-%m-%d")
        end = datetime.strptime(end_date,"%Y-%m-%d")
        filters.append(Transaction.date.between(start,end))

    if max_amount is not None and int(max_amount) == 0:
        filters.append(Transaction.amount > 500)
    elif max_amount is not None:
        filters.append(Transaction.amount < max_amount)

    statement = select(Transaction).where(*filters)
    transactions = db.session.execute(statement).scalars().all()
  
    return jsonify([{
        'id': t.id,
        'date': t.date,
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'description': t.description
    } for t in transactions])
