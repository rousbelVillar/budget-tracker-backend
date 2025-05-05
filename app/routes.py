from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import Transaction
from . import db

main = Blueprint('main', __name__)

@main.route('/transactions', methods=['GET'])
def get_transactions():
    #month = request.args.get()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    # transactions = list(transactions_collections.find({},{'_id':0}))
    # if month:
    #     year, mon = map(int,month.split('-'));
    #     transactions = [
    #         t for t in transactions
    #         if 'date' in t and datetime.strptime(t['date'], '%Y-%m-%d').year == year
    #         and datetime.strptime(t['date'], '%Y-%m-%d').month == mon
    #     ]
    return jsonify([{
        'id': t.id,
        'amount': t.amount,
        'type': t.type,
        'category': t.category,
        'note': t.note,
        'description': t.description,
        'date': t.date.isoformat()
    } for t in transactions])
    return jsonify(transactions)

@main.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    t = Transaction(
        amount=data['amount'],
        type=data['type'],
        category=data['category'],
        description=data.get('description'),
        note=data.get('note', ''),
        # date=data.get('date')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'id': t.id}), 201

@main.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted'})
