from flask import Flask, jsonify, request
from flask_cors import CORS
from db.firebase_db import get_balance, deposit, withdraw
import traceback


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/balance/<user_id>', methods=['GET'])
def route_get_balance(user_id):
    result = get_balance(user_id)
    if result is not None:
        return jsonify({'balance': result})
    return jsonify({'error': 'User not found'}), 404

@app.route('/deposit', methods=['POST'])
def route_deposit():
    try:
        data = request.get_json()
        result = deposit(data['user_id'], data['amount'])
        if not isinstance(result, dict):
            return jsonify({'error': 'Unexpected error'}), 500
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        # Log the exception or handle it as needed
        print("Error in /deposit route:", e)
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/withdraw', methods=['POST'])
def route_withdraw():
    data = request.get_json()
    result = withdraw(data['user_id'], data['amount'])
    if not isinstance(result, dict):
        return jsonify({'error': 'Unexpected error'}), 500
    if 'error' in result:
        status_code = 400 if result.get('error') == 'Insufficient funds' else 404
        return jsonify(result), status_code
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
