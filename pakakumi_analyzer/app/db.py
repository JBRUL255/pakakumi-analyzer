import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        conn = sqlite3.connect("data.db")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS rounds (
            id SERIAL PRIMARY KEY,
            crash_point REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def insert_round(crash_point: float):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO rounds (crash_point) VALUES (%s);", (crash_point,))
    conn.commit()
    conn.close()

def get_latest_rounds(limit: int = 100):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT crash_point FROM rounds ORDER BY id DESC LIMIT %s;", (limit,))
    rows = c.fetchall()
    conn.close()
    return [row["crash_point"] for row in rows]
