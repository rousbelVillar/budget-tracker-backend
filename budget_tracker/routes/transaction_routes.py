#transactions_routes.py

from flask import request, jsonify, session
from ..models.transaction_models import db, Transaction
from flask import Blueprint

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    t = Transaction(
        type=data['type'],
        amount=data['amount'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'id': t.id}), 201

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    t = Transaction.query.get(transaction_id)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    month = request.args.get('month')
    print('month',month)
    query = Transaction.query
    if month:
        query = query.filter(Transaction.date.startswith(month))
    user_id = session.get('user_id')
    transactions = Transaction.query.filter_by(user_id=user_id).all()    
    return jsonify([{
        'id': t.id,
        'date': t.date,
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'description': t.description
    } for t in transactions])