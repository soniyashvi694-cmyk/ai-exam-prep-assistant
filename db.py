import os
import sqlite3
import hashlib
import secrets

DB_FILE = os.path.join(os.path.dirname(__file__), "exam_prep.db")


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()


def register_user(username, password):
    username = username.strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (username, password_hash, salt),
        )
        conn.commit()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, salt FROM users WHERE username = ?",
                (username.strip(),))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None
    user_id, stored_hash, salt = row
    if hash_password(password, salt) == stored_hash:
        return {"id": user_id, "username": username.strip()}
    return None


def save_plan(user_id, title, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO plans (user_id, title, content) VALUES (?, ?, ?)",
                (user_id, title, content))
    conn.commit()
    conn.close()


def get_plans(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, content, created_at FROM plans WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def init_quiz_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT,
            topic TEXT,
            difficulty TEXT,
            score INTEGER,
            total INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def save_result(user_id, subject, topic, difficulty, score, total):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quiz_results (user_id, subject, topic, difficulty, score, total) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, subject, topic, difficulty, score, total),
    )
    conn.commit()
    conn.close()


def get_results(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT subject, topic, difficulty, score, total, created_at "
        "FROM quiz_results WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows