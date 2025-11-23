import sqlite3
import os

# Absolute path to database file
DB_NAME = os.path.join(os.path.dirname(__file__), "password_manager.db")

#this is the logic that creates the database table
def initialize_database():
    """Creates the database and tables from schema.sql if not already present."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_file, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

#this gets the database connected to the application
def get_connection():
    """Helper function to open a database connection."""
    return sqlite3.connect(DB_NAME)

