import pandas as pd
import json
import os
import requests 
import matplotlib.pyplot as plt 

# --- Configuration (Adjust these as needed) ---
# Load from a local JSON file (if you ran the curl command)
# JSON_FILE_PATH = 'transactions_data.json'

# Fetch directly from your Flask API
API_BASE_URL = "http://127.0.0.1:5001" # Ensure this matches Flask app's port
USER_ID_TO_ANALYZE = "1" # Replace with an actual user_id from data

# Define the directory to save the generated plots
# This assumes 'analysis' folder is peer to 'backend', and plots go into backend/static/images
PLOT_SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'backend', 'static', 'images')
PLOT_FILENAME = 'transaction_summary.png'
PLOT_PATH = os.path.join(PLOT_SAVE_DIR, PLOT_FILENAME)

# Create the directory if it doesn't exist
os.makedirs(PLOT_SAVE_DIR, exist_ok=True)


# --- Data Loading (Choose ONE of these options) ---
df = pd.DataFrame() # Initialize an empty DataFrame

# Load from a local JSON file
# Uncomment this block if you are using 'curl' to save data to JSON_FILE_PATH
# if os.path.exists(JSON_FILE_PATH):
#     try:
#         with open(JSON_FILE_PATH, 'r') as f:
#             transactions_json = json.load(f)
#         print(f"Successfully loaded data from {JSON_FILE_PATH}")
#         df = pd.DataFrame(transactions_json)
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON from {JSON_FILE_PATH}: {e}")
#         print("Please ensure the file contains valid JSON.")
#     except Exception as e:
#         print(f"An unexpected error occurred during file load: {e}")
# else:
#     print(f"JSON file not found at {JSON_FILE_PATH}. Skipping file load.")
#     print("Consider running the 'curl' command first or using Option 2 (direct API fetch).")


# Fetch data directly from Flask API
# Uncomment this block to pull fresh data from your API every time
api_url = f"{API_BASE_URL}/transactions/{USER_ID_TO_ANALYZE}"
try:
    response = requests.get(api_url)
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
    transactions_json = response.json()

    print(f"Successfully fetched data from {api_url}")

    if not transactions_json:
        print(f"No transactions found for user_id: {USER_ID_TO_ANALYZE}.")
        df = pd.DataFrame() # Create an empty DataFrame
    else:
        df = pd.DataFrame(transactions_json)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
    print("Please ensure your Flask app is running on the correct port and the user_id is valid.")
    df = pd.DataFrame() # Ensure df is empty on error
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    print("The API might not have returned valid JSON.")
    df = pd.DataFrame() # Ensure df is empty on error
except Exception as e:
    print(f"An unexpected error occurred during API fetch: {e}")
    df = pd.DataFrame() # Ensure df is empty on error


# --- Perform Analysis only if DataFrame is not empty ---
if not df.empty:
    print("\n--- DataFrame Loaded ---")
    print("DataFrame Head (first 5 rows):")
    print(df.head())
    print("\nDataFrame Info (data types and non-null counts):")
    print(df.info())

    # Ensure 'timestamp' column is datetime for time-based operations
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- Q1: What is the total number of deposits and withdrawals for each user? ---
    print("\n--- Q1: Total Number of Deposits and Withdrawals for Each User ---")
    # Group by user_id and transaction type, then count the occurrences
    transaction_counts = df.groupby(['user_id', 'type']).size().unstack(fill_value=0)
    # Rename columns for clarity (optional, if 'deposit'/'withdraw' are already good)
    transaction_counts.columns.name = 'Transaction Type'
    print(transaction_counts)

    # --- Q2: What is the average transaction amount by transaction type? ---
    print("\n--- Q2: Average Transaction Amount by Transaction Type ---")
    # Group by transaction type and calculate the mean of the 'amount'
    average_amount_by_type = df.groupby('type')['amount'].mean()
    print(average_amount_by_type)

    # --- Generate and Save a Graph ---
    print("\n--- Generating and Saving Graph ---")
    try:
        # Prepare data for plotting (using Q1 data for a simple bar chart)
        # need to flatten the transaction_counts for plotting if there are multiple users
        plot_data = df.groupby('type')['amount'].sum() # Sum of amounts by type
        
        plt.figure(figsize=(8, 5))
        plot_data.plot(kind='bar', color=['lightgreen', 'salmon'])
        plt.title(f'Total Transaction Amounts by Type for User: {USER_ID_TO_ANALYZE}')
        plt.xlabel('Transaction Type')
        plt.ylabel('Total Amount ($)')
        plt.xticks(rotation=0) # Keep labels horizontal
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() # Adjust layout to prevent labels from being cut off

        # Save the plot to the specified path
        plt.savefig(PLOT_PATH)
        print(f"Graph saved successfully to: {PLOT_PATH}")
        plt.close() # Close the plot to free memory

    except Exception as e:
        print(f"Error generating or saving graph: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging graph issues


    # --- Further analysis examples (from previous conversation) ---
    print("\n--- Optional: Further Analysis Examples ---")

    # Calculate Total Deposits
    deposits_df = df[df['type'] == 'deposit']
    total_deposits = deposits_df['amount'].sum()
    print(f"\nTotal Deposits: ${total_deposits:.2f}")

    # Calculate Total Withdrawals
    withdrawals_df = df[df['type'] == 'withdraw']
    total_withdrawals = withdrawals_df['amount'].sum()
    print(f"\nTotal Withdrawals: ${total_withdrawals:.2f}")

    # Calculate Current Balance (from transactions)
    current_balance_from_txns = df[df['type'] == 'deposit']['amount'].sum() - \
                                df[df['type'] == 'withdraw']['amount'].sum()
    print(f"\nCalculated Balance from Transactions: ${current_balance_from_txns:.2f}")

    # Transactions Over Time (Daily Summary)
    # Ensure 'timestamp' is converted to datetime before accessing .dt
    if 'timestamp' in df.columns:
        df['date_only'] = df['timestamp'].dt.date # Create a new column with just the date
        daily_summary = df.groupby(['date_only', 'type'])['amount'].sum().unstack(fill_value=0)
        # Handle cases where 'deposit' or 'withdraw' columns might not exist if no such transactions
        daily_summary['net_flow'] = daily_summary.get('deposit', 0) - daily_summary.get('withdraw', 0)
        print("\nDaily Financial Summary:")
        print(daily_summary)


    # --- Export to CSV (optional) ---
    output_csv_file = 'transactions_analysis_report.csv'
    df.to_csv(output_csv_file, index=False)
    print(f"\nProcessed DataFrame successfully saved to {output_csv_file}")

else:
    print("\nDataFrame is empty. No analysis performed.")

