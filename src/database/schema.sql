-- database/schema.sql

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    masterpassword BLOB,
    passwords TEXT DEFAULT '[]' 
);
