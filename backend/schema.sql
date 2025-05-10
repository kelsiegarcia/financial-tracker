CREATE table users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	balance REAL DEFAULT 0.0
);

-- insert first intial user 
INSERT INTO users (id, balance) VALUES (1, 100.0);

