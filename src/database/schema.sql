-- database/schema.sql

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    masterpassword TEXT NOT NULL,
    passwords TEXT
);
