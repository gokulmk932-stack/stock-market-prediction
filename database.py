import sqlite3
import hashlib


# Database Connection
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn


# Password Hashing
def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# Create Users Table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


# Register User
def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users(username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password)
        )

        conn.commit()
        result = True

    except sqlite3.IntegrityError:
        result = False

    finally:
        conn.close()

    return result


# Login Check
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hashed_password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return True

    return False


# Create database when file runs
create_table()
