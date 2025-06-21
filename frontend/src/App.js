import React from 'react';
import logo from './financial.jpg';
import './App.css';
import BalanceDisplay from './BalanceDisplay.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p></p>
        <BalanceDisplay />
        <img
          src="http://127.0.0.1:5001/static/images/transaction_summary.png"
          alt="Transaction Summary Graph"
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </header>
    </div>
  );
}

export default App;
