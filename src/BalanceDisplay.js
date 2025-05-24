import React, { useEffect, useState } from 'react';

function BalanceDisplay() {
  const userId = '1';
  const API_BASE = 'http://localhost:5001';
  // state variable to store the balance input initialized to an empty string
  // useState is a Hook that lets you add React state to function components
  // useState returns an array with two elements: the current state value and a function to update it
  const [balanceInput, setBalanceInput] = useState('');

  // state variable to store the current balance initialized to 0
  const [currentBalance, setCurrentBalance] = useState(0);

  // keeps track of the transaction type (either deposit or withdraw) for buttons
  // initialized to 'deposit'
  const [transactionType, setTransactionType] = useState('deposit');

  // set message
  const [message, setMessage] = useState('');

  //set error message
  const [error, setError] = useState('');

  // fetch balance on load
  // useEffect is a Hook that lets you perform side effects in function components
  // it runs after the first render and after every update
  // the empty array [] means it runs only once after the initial render
  // it fetches the balance from the server using the userId
  // if the balance is successfully fetched, it updates the currentBalance state variable
  // if there is an error, it sets the error state variable

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await fetch(`${API_BASE}/balance/${userId}`);
        const data = await response.json();
        if (data.balance !== undefined) {
          setCurrentBalance(data.balance);
        } else {
          setError(data.error || 'Error fetching balance');
        }
      } catch (error) {
        setError('Failed to connect to server');
      }
    };

    fetchBalance();
  }, [userId]);

  // function to handle the balanceInput state in sync with the input field
  // event.target.value gets the value of the input field from the html
  const handleBalanceInputChange = (event) => {
    setBalanceInput(event.target.value);
  };

  // function to handle the transaction type in sync with the radio buttons
  // event.target.value gets the value of the radio button from the html
  const handleTransaction = (event) => {
    event.preventDefault();
    try {
      const amount = parseFloat(balanceInput);

      // check if the amount is a valid number
      if (isNaN(amount)) {
        alert('Please enter a valid number');
        return;
      }
      if (amount <= 0) {
        setError('Please enter a valid positive number');
        return;
      }
      if (transactionType === 'deposit') {
        setCurrentBalance((prevBalance) => prevBalance + amount);
      } else if (transactionType === 'withdraw') {
        if (amount <= currentBalance) {
          setCurrentBalance((prevBalance) => prevBalance - amount);
        } else {
          alert('Insufficient funds.');
          return;
        }
      } else {
        alert('Please enter a valid number for the transaction amount');
      }
      setBalanceInput(''); // Clear the input after transaction

      const endpoint = transactionType === 'deposit' ? 'deposit' : 'withdraw';

      // make a POST request to the server with the userId and amount
      fetch(`${API_BASE}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          amount,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log('server response:', data);
          if (data.balance !== undefined) {
            setCurrentBalance(data.balance);
            setMessage(data.message || `${transactionType} successful`);
            setError('');
            setBalanceInput('');
          } else {
            setError(data.error || 'Transaction failed');
            setMessage('');
          }
        })
        .catch(() => setError('Failed to connect to server'));
    } catch (error) {
      console.error('An error occurred:', error);
      setError('An unexpected error occurred. Please try again.');
    }
  };

  // event handlers for updating transactionType state variable. it keeps track of the transaction type (either deposit or withdraw).
  // influences the text on the submit button and the login for handleTransaction function
  const selectDeposit = () => {
    setTransactionType('deposit');
    setMessage('');
    setError('');
  };

  const selectWithdraw = () => {
    setTransactionType('withdraw');
    setMessage('');
    setError('');
  };

  // dynamically renders the button text based on the transactionType state variable
  return (
    <div>
      <h2>Account Balance Tracker</h2>
      <p>
        Current Balance:{' '}
        <span style={{ fontWeight: 'bold' }}>${currentBalance.toFixed(2)}</span>
      </p>

      <div>
        <button
          onClick={selectDeposit}
          className={transactionType === 'deposit' ? 'active' : ''}
        >
          Deposit
        </button>
        <button
          onClick={selectWithdraw}
          className={transactionType === 'withdraw' ? 'active' : ''}
        >
          Withdraw
        </button>
      </div>

      <form onSubmit={handleTransaction}>
        <div>
          <label htmlFor="transactionAmount">Enter Amount:</label>
          <input
            type="text"
            id="transactionAmount"
            value={balanceInput}
            onChange={handleBalanceInputChange}
            placeholder="e.g., 50.00"
          />
        </div>
        <button type="submit">
          {transactionType === 'deposit' ? 'Deposit Amount' : 'Withdraw Amount'}
        </button>
      </form>
    </div>
  );
}

export default BalanceDisplay;
