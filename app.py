from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Transaction

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Routes
@app.route('/transactions', methods=['GET'])
def get_transactions():
    month = request.args.get('month')  # e.g., '2025-05'
    query = Transaction.query
    if month:
        query = query.filter(Transaction.date.startswith(month))
    transactions = query.all()
    return jsonify([{
        'id': t.id,
        'date': t.date,
        'type': t.type,
        'amount': t.amount,
        'category': t.category
    } for t in transactions])

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    t = Transaction(
        date=data['date'],
        type=data['type'],
        amount=data['amount'],
        category=data['category']
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Transaction added', 'id': t.id}), 201

@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    t = Transaction.query.get(transaction_id)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
