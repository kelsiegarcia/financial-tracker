import firebase_admin
from firebase_admin import credentials, firestore
import os
import traceback
# Compute absolute path to the JSON credentials file relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "..", "firebase", "firebase_credentials.json")
cred = credentials.Certificate(cred_path)



if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
# Only initialize once
if not firebase_admin._apps:
    cred = credentials.Certificate("../firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_balance(user_id):
	try:
		doc_ref = db.collection("users").document(str(user_id))
		doc = doc_ref.get()
		if doc.exists:
			return doc.to_dict().get("balance", 0.0)
		else:
			# Auto-create user with zero balance if missing
			doc_ref.set({"balance": 0.0})
			return 0.0
	except Exception as e:
		print("Error in get_balance function:", e)
		traceback.print_exc()
		return {"error": "Unexpected error"}


def deposit(user_id, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "Amount must be positive"}

        doc_ref = db.collection("users").document(str(user_id))
        doc = doc_ref.get()

        if doc.exists:
            current_balance = doc.to_dict().get("balance", 0.0)
            new_balance = current_balance + amount
            doc_ref.update({"balance": new_balance})
        else:
            new_balance = amount
            doc_ref.set({"balance": new_balance})

        return {
            "balance": new_balance,
            "message": f"Deposited ${amount:.2f} successfully."
        }
    except Exception as e:
        print("Error in deposit function:", e)
        traceback.print_exc()
        return {"error": "Unexpected error"}


def withdraw(user_id, amount):
	try:
		amount = float(amount)
		if amount <= 0:
			return {"error": "Amount must be positive"}

		doc_ref = db.collection("users").document(str(user_id))
		doc = doc_ref.get()

		if not doc.exists:
			return {"error": "User does not exist"}

		current_balance = doc.to_dict().get("balance", 0.0)
		new_balance = current_balance - amount

		if new_balance < 0:
			return {"error": "Insufficient funds"}

		doc_ref.update({"balance": new_balance})
		return {
			"balance": new_balance,
			"message": f"Withdrew ${amount:.2f} successfully."
		}
	except Exception as e:
		print("Error in withdraw function:", e)
		traceback.print_exc()
		return {"error": "Unexpected error"}
