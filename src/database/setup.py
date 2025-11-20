# database/setup.py

import sqlite3
import os

DB_NAME = "password_manager.db"
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")


#this is the logic that creates the database table
def initialize_database():
    """Creates the database and tables from schema.sql if not already present."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print(" Database initialized successfully.")


#this gets the dtabase connected to the application
def get_connection():
    """Helper function to open a database connection."""
    return sqlite3.connect(DB_NAME)

