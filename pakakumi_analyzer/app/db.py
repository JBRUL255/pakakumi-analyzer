# pakakumi_analyzer/app/db.py
import sqlite3
import os
from pakakumi_analyzer.app.config import DB_PATH

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cashout REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_round(cashout: float):
    conn = get_db()
    conn.execute("INSERT INTO rounds (cashout) VALUES (?)", (cashout,))
    conn.commit()
    conn.close()

def get_latest_rounds(limit=50):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT cashout FROM rounds ORDER BY id DESC LIMIT ?", (limit,))
    rows = [row["cashout"] for row in cur.fetchall()]
    conn.close()
    return rows

def get_all_rounds():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT cashout FROM rounds")
    rows = [row["cashout"] for row in cur.fetchall()]
    conn.close()
    return rows
