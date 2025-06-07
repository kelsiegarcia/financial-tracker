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
      </header>
    </div>
  );
}

export default App;
