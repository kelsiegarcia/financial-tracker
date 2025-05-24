from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


DATABASE = 'mydatabase.db'

# function to get a database connection
# this function creates a connection to the SQLite database
# and sets the row factory to sqlite3.Row
def get_db():
  conn = sqlite3.connect(DATABASE)
  # set the row factory to sqlite3.Row to access columns by name
	# this allows us to access the columns by name instead of index
  conn.row_factory = sqlite3.Row
  return conn


# function to close the database connection
def close_db(conn):
  if conn:
    conn.close()

# function to create the database schema
def init_db():
  conn = get_db()
  with open('schema.sql') as f:
    conn.executescript(f.read())
  close_db(conn)
  
# function to initialize the database
@app.cli.command('initdb')
def init_db_command():
  init_db()
  print('Initialized the database.')

# route and dev server
# define a route for the flask app. route listents for HTTP GET requests at the root URL with user_id as a dynamic parameter
@app.route('/balance/<user_id>', methods=['GET'])

# function to get the balance of a user
def get_balance(user_id):
  #connect to the database
	# and retrieve the balance of the user with the given user_id
  conn = get_db()
  user = conn.execute('SELECT balance FROM users WHERE id = ?', (user_id,)).fetchone()
  close_db(conn)
  # check if the user exists in the database
	# if user exists, return/response the balance in JSON format
  # if user does not exist, return an error message
  if user:
    return jsonify({'user_id': user_id, 'balance': user['balance']})
  return jsonify({'error': 'User not found'}), 404

# route for depositing funds
@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']

    conn = get_db()
    user = conn.execute('SELECT balance FROM users WHERE id = ?', (user_id,)).fetchone()

    if user:
        new_balance = user['balance'] + amount
        conn.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
        conn.commit()
        close_db(conn)
        return jsonify({'message': 'Deposit successful', 'balance': new_balance})

    close_db(conn)
    return jsonify({'error': 'User not found'}), 404


@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']

    conn = get_db()
    user = conn.execute('SELECT balance FROM users WHERE id = ?', (user_id,)).fetchone()

    if user:
        if amount > user['balance']:
            close_db(conn)
            return jsonify({'error': 'Insufficient funds'}), 400
        new_balance = user['balance'] - amount
        conn.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
        conn.commit()
        close_db(conn)
        return jsonify({'message': 'Withdrawal successful', 'balance': new_balance})

    close_db(conn)
    return jsonify({'error': 'User not found'}), 404

  


# run the app in debug mode

if __name__ == '__main__':
  app.run(debug=True, port=5001)
  