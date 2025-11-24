# database/db_logic.py

# --------------------------------------------------
# This file handles all database operations:
# - User registration
# - Login authentication
# - Encrypting and saving passwords
# - Decrypting stored passwords
# --------------------------------------------------

import sqlite3
import bcrypt
import json
import base64
from cryptography.fernet import Fernet
from database.setup import get_connection


# --------------------------------------------------
# HELPER: Derive encryption key from the master password
# --------------------------------------------------
def derive_key(master_password: str) -> Fernet:
    """
    Derives a Fernet encryption key from the user's master password.
    Uses bcrypt hashing output as a salt-like transformation.

    NOTE:
    - This is NOT a true KDF (like PBKDF2 or scrypt) but modeled for project-level security.
    - Bcrypt output is 60 bytes, Fernet requires 32-byte base64 key → so we slice + base64 encode.
    """
    hashed = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())
    key = hashed[:32]  # use first 32 bytes
    return Fernet(base64.urlsafe_b64encode(key))


# --------------------------------------------------
# REGISTER USER (stores hashed master password)
# --------------------------------------------------
def register_user(username: str) -> bool:
    """
    Registers a new user by inserting a row with masterpassword NULL and an empty passwords list.
    Returns:
        True if successful
        False if username already exists
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, masterpassword, passwords) VALUES (?, ?, ?)",
            (username, None, json.dumps([]))
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # Username already exists
        return False

    finally:
        conn.close()


# --------------------------------------------------
# LOGIN USER (username-only login)
# --------------------------------------------------
def login_user(username: str):
    """
    Logs in a user using username only.
    Returns:
        (True, stored_master) if user exists (stored_master may be None)
        (False, None) if user does not exist
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT masterpassword FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, None

    stored_master = row[0]  # may be None if master not set yet
    return True, stored_master


# --------------------------------------------------
# SAVE ENCRYPTED USER PASSWORD (no label; stored as list)
# FIRST SAVED PASSWORD BECOMES MASTER PASSWORD
# --------------------------------------------------
def save_user_password(username: str, password: str) -> bool:
    """
    Saves the password into the user's password list (JSON list).
    If the user's masterpassword is not set (NULL), this first password becomes the master password.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT passwords, masterpassword FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    stored_pw_json, stored_master = row

    # Load as list (if empty or null, create empty list)
    try:
        current_pw_list = json.loads(stored_pw_json) if stored_pw_json else []
        if not isinstance(current_pw_list, list):
            # If for some reason it's a dict (legacy), convert values to list
            current_pw_list = list(current_pw_list.values())
    except Exception:
        current_pw_list = []

    # If masterpassword is not set yet, this first saved password becomes the master
    if stored_master is None:
        hashed_master = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute(
            "UPDATE users SET masterpassword=? WHERE username=?",
            (hashed_master, username)
        )
        fernet_key = derive_key(password)
    else:
        # Build Fernet key from stored_master by slicing first 32 bytes (project-workaround)
        key_material = stored_master[:32]
        fernet_key = Fernet(base64.urlsafe_b64encode(key_material))

    # Encrypt new password and append to list
    encrypted = fernet_key.encrypt(password.encode()).decode()
    current_pw_list.append(encrypted)

    cursor.execute(
        "UPDATE users SET passwords=? WHERE username=?",
        (json.dumps(current_pw_list), username)
    )

    conn.commit()
    conn.close()
    return True


# --------------------------------------------------
# GET DECRYPTED PASSWORD LIST
# --------------------------------------------------
def get_saved_passwords(username: str, stored_master):
    """
    Retrieves all saved passwords and decrypts them.
    Returns a list of plaintext passwords in order (or an empty list).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT passwords FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row or not row[0]:
        return []

    # If there is no stored_master (None), we cannot decrypt — return empty list
    if stored_master is None:
        return []

    try:
        encrypted_list = json.loads(row[0])
        if not isinstance(encrypted_list, list):
            # If stored as dict by older code, convert to list of values
            encrypted_list = list(encrypted_list.values())
    except Exception:
        return []

    # Reconstruct fernet key from stored_master (project workaround)
    key_material = stored_master[:32]
    fernet_key = Fernet(base64.urlsafe_b64encode(key_material))

    decrypted = []
    for enc_pw in encrypted_list:
        try:
            decrypted.append(fernet_key.decrypt(enc_pw.encode()).decode())
        except Exception:
            decrypted.append("(decryption failed)")

    return decrypted
