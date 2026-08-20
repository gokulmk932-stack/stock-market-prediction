import sqlite3


# Database Connection
def create_connection():

    conn = sqlite3.connect("users.db")

    return conn



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

        cursor.execute(
            """
            INSERT INTO users(username, password)
            VALUES (?,?)
            """,
            (username, password)
        )

        conn.commit()

        result = True

    except sqlite3.IntegrityError:

        result = False


    conn.close()

    return result



# Login Check
def login_user(username, password):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )


    user = cursor.fetchone()

    conn.close()


    if user:

        return True

    else:

        return False



# Create database when file runs
create_table()
