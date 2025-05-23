# Financial Tracker

## Overview

The **Financial Tracker** is a full-stack application designed to help users manage a personal balance by performing deposit and withdrawal transactions. It is built with a **React frontend**, a **Flask backend**, and a **SQLite3 database** to persist financial data.

As a software engineer, this project helped me deepen my understanding of RESTful APIs, state management in React, full-stack data flow, and basic networking concepts. It also provided experience working with database integration and frontend/backend communication using HTTP over TCP.

### Software Demo Video

[Watch Demo](http://youtube.link.goes.here)

## Web App Features

- Built with React (served at `http://localhost:3000`)
- View and update account balance in real time
- Select between **deposit** or **withdraw**
- Input numeric values for transactions
- Balance is updated dynamically
- User is alerted on:
  - Invalid inputs
  - Insufficient funds
- Clear feedback and interaction via modern UI

## Network Communication

This application uses a **Client-Server** architecture with HTTP requests over **TCP** (in may case, port `5001` on the backend and `3000` on the frontend).

### Message Flow:

- `GET /balance/<user_id>` — Retrieve the user's current balance
- `POST /deposit` — Deposit an amount into the account
- `POST /withdraw` — Withdraw an amount from the account

**Message Format:** JSON (for both requests and responses)

```json
// Example request
{
  "user_id": 1,
  "amount": 20
}

// Example response
{
  "balance": 120.0
}
```

### Server Setup

To run the Flask server (on port 5001, in my case):

```bash
flask --app backend/app.py run
```

### Client Setup

To run the React frontend (on port 3000 by default):

```bash
cd frontend
npm install
npm start
```

Ensure Flask and React are running simultaneously.

## Development Environment

**Frontend:**

- React
- JSX
- CSS
- npm

**Backend:**

- Flask (Python)
- SQLite3 (Database)

**Tools Used:**

- Visual Studio Code
- Postman (for API testing)
- curl (for manual HTTP requests)

## Useful Websites

- [React Documentation](https://reactjs.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MDN Web Docs](https://developer.mozilla.org/)
- [TutorialsPoint - React](https://www.tutorialspoint.com/reactjs/)

## Future Work

- ✅ Connect frontend to Flask backend (Completed)
- ✅ Add database persistence using SQLite (Completed)
- ✅ Support multiple transaction types (Completed)
- 🔲 Display full transaction history from database
- 🔲 Add savings goals with progress bars
- 🔲 Implement authentication for multiple users
- 🔲 Deploy project to a cloud platform
