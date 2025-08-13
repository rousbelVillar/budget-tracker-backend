#transactions_routes.py

from datetime import date, datetime
import random
from faker import Faker
from flask import request, jsonify
import pytz
from sqlalchemy import func
from ..models.transaction_models import db, Transaction
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity


transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/add', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.json.get("params")
    tz_ny = pytz.timezone('America/Los_Angeles')
    now_la = datetime.now(tz_ny)
    t = Transaction(
        type=data['type'],
        amount=data['amount'],
        category=data['category'],
        description=data['description'],
        user_id=user_id,
        date=now_la
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'id': t.id}), 201

@transaction_bp.route('/bulk/add', methods=['POST'])
@jwt_required()
def add_bulk_transactions():
    user_id = get_jwt_identity()
    transactions_data = request.get_json()
    fake = Faker()

    if not isinstance(transactions_data, list):
        return jsonify({"error": "Expected a list of transactions"}), 400

    transactions = []
    for entry in transactions_data:
        try:
            fake_date = fake.date_time_this_year()
            fake_date = fake_date.replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            transaction = Transaction(
                amount=entry['amount'],
                type=entry['type'],
                category=entry['category'],
                description=entry.get('description', ''),
                user_id=user_id,
                date= fake_date
            )
            transactions.append(transaction)
        except KeyError as e:
            return jsonify({"error": f"Missing field {str(e)}"}), 400

    db.session.add_all(transactions)
    db.session.commit()

    return jsonify({"message": f"{len(transactions)} transactions added"}), 201

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
    categories = request.args.get('categories')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')

    query = db.session.query(Transaction)

    if start_date and end_date:
        try:
            start_date = date(int(start_date.split("-")[0]),int(start_date.split("-")[1]),int(start_date.split("-")[2]))
            end_date = date(int(end_date.split("-")[0]),int(end_date.split("-")[1]),int(end_date.split("-")[2]))
            query = query.filter(Transaction.date.between(start_date,end_date))
        except ValueError:
            return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    if min_amount:
        query = query.filter(Transaction.amount >= float(min_amount))
    if max_amount:
        query = query.filter(Transaction.amount <= float(max_amount))

    if categories:
        categories_list = categories.split(",")
        query = query.filter(Transaction.category.in_(categories_list))
        
    query = query.filter(Transaction.is_deleted == False, Transaction.user_id == user_id)
    transactions = query.order_by(Transaction.date.desc()).all()

    return jsonify([{
        'id': t.id,
        'date': t.date.isoformat() if t.date else None,
        'type': t.type,
        'amount': t.amount,
        'category': t.category,
        'description': t.description
    } for t in transactions])
