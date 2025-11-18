## Setup and Running Instructions

### 1. Install Required Libraries
Open a terminal in your project root (e.g., `C:\CSC455\CSC455Project`) and run:

```powershell
pip install streamlit bcrypt pandas
```

### 2. Running the App
From the project root, run:
Or, if you are in the `src` folder:

```powershell
streamlit run main.py
```

This will launch the app in your browser (usually at http://localhost:8501).

### 3. Code Structure and Changes
- The circular import between `main.py` and `hash.py` has been removed.
- The function `HashPassword()` in `hash.py` is now only called when explicitly invoked (not on import).
- The main app logic is in `main.py` and the UI is handled in `gui.py` using Streamlit.

### 4. Troubleshooting
- If you see warnings about Streamlit, make sure you are running the app with `streamlit run ...` as above.
- If you get ImportError, check that all required packages are installed.

---
### 5. Adding a Database with SQLite

You can use SQLite to store passwords or user data for your app. Here’s how to get started:

**a. Install SQLite support (if needed):**
Python’s standard library includes `sqlite3`, so no extra install is needed. If you want a GUI for browsing the database, try [DB Browser for SQLite](https://sqlitebrowser.org/).

**b. Basic usage example:**
Add this to your code (e.g., in `gui.py` or a new `db.py`):

```python
import sqlite3

# Connect to a database file (creates it if it doesn't exist)
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# Create a table (run once)
cursor.execute('''
	CREATE TABLE IF NOT EXISTS passwords (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT,
		password TEXT
	)
''')
conn.commit()

# Example: insert a password
cursor.execute('INSERT INTO passwords (username, password) VALUES (?, ?)', ("user1", "secret"))
conn.commit()

# Example: fetch passwords
cursor.execute('SELECT * FROM passwords')
print(cursor.fetchall())

# Always close the connection when done
conn.close()
```

**c. Integrate with Streamlit:**
- Place database code in a function or a separate module (e.g., `db.py`).
- Use Streamlit widgets to collect user input and call your database functions.
- Always commit changes and close the connection when finished.

**d. Security note:**
- Never store plain text passwords. Always hash passwords before saving (use your `hash.py` logic).

**e. More info:**
- See the [Python sqlite3 docs](https://docs.python.org/3/library/sqlite3.html) for more details.

---
### 6. Using the Project Database

Your project includes a `database` folder with code to set up and use a SQLite database (`password_manager.db`).

**a. Initialize the database:**
Before running the app for the first time, initialize the database tables by running:

```powershell
cd src/database
py -3 setup.py
```
This will create `password_manager.db` in the `src/database` folder with the required tables.

**b. Database schema:**
- `users` table: stores user accounts (id, username, masterpassword)
- `passwords` table: stores saved passwords (id, user_id, site, username, password)


---