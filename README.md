# 💰 Financial Tracker Web App

## Overview

This project is a personal finance tracker web application that allows users to view their balance, deposit funds, and withdraw money. It’s part of a long-term learning effort to strengthen my skills as a full-stack software engineer. There is a strong focus on modular development, data persistence, and cloud integration.

The project is built using **React** for the frontend, **Flask** for the backend API, and **Firebase Realtime Database** for cloud-based storage in Module 3. In earlier modules, I explored state management with JavaScript (Module 1) and integrated a local SQLite3 database (Module 2).

📹 [Software Demo Video](https://youtu.be/Mq-4ct8IneM)

---

## 📦 Modules Overview

### ✅ Module 1: Frontend Development

- Created a functional UI using **React** with state and form handling.
- Added logic for handling transactions (deposit, withdraw) in-memory.
- Set up project structure with React Hooks.

### ✅ Module 2: Backend Integration with Local DB

- Set up a **Flask** backend and connected it to a **SQLite3** database.
- API endpoints created for:
  - `GET /balance/:user_id`
  - `POST /deposit`
  - `POST /withdraw`
- Data was persisted locally with `sqlite3`.

### ✅ Module 3: Cloud Database with Firebase

- Migrated backend database logic to **Firebase Realtime Database**.
- Updated endpoints to interact with Firebase instead of SQLite.
- Deployed project in a way that reflects scalable cloud practices.

---

## ☁️ Cloud Database

- **Firebase Realtime Database**
- Secure access set up using service account credentials (`firebase_credentials.json`)
- Database structure (per user):
  ```json
  {
    "users": {
      "1": {
        "balance": 1000
      },
      "2": {
        "balance": 500
      }
    }
  }
  ```

---

## 💻 Development Environment

- **Frontend:** React, JavaScript
- **Backend:** Flask, Python 3
- **Database:** Firebase Realtime DB (Module 3), SQLite (Module 2)
- **Tools:** VS Code, Firebase Console, GitHub

---

## 🔗 Useful References

- [Firebase Realtime Database Docs](https://firebase.google.com/docs/database)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Official Docs](https://reactjs.org/)
- [Vite](https://vitejs.dev/)

---

## 🚀 Future Improvements

- Add user authentication with Firebase Auth
- Track transaction history per user
- Add styling and UI animations
- Validate numeric inputs and show real-time errors
- Allow multiple users with login functionality

---
