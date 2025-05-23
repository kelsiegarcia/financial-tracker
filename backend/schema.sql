-- This file contains the SQL schema for the financial tracker application.
-- It defines the structure of the database tables and their relationships.
-- The schema includes a table for users and a table for transactions.
-- The transactions table is linked to the users table through a foreign key.
-- The schema is designed to support the functionality of tracking financial transactions
-- and managing user balances.
CREATE table users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	balance REAL DEFAULT 0.0
);

-- insert first intial user 
INSERT INTO users (id, balance) VALUES (1, 100.0);

