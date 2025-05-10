from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'mydatabase.db'


# function to create the database and table
def get_db():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn

def close_db(conn):
  if conn:
    conn.close()

def init_db():
  conn = get_db()
  with open('schema.sql') as f:
    conn.executescript(f.read())
  close_db(conn)

@app.cli.command('initdb')
def init_db_command():
  init_db()
  print('Initialized the database.')

# route and dev server
@app.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
  conn = get_db()
  user = conn.execute('SELECT balance FROM users WHERE id = ?', (user_id,)).fetchone()
  close_db(conn)
  if user:
    return jsonify({'user_id': user_id, 'balance': user['balance']})
  return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
  app.run(debug=True)