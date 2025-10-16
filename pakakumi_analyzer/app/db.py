# pakakumi_analyzer/app/db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    """
    Returns a new PostgreSQL database connection.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """
    Create the table if it doesn't exist.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rounds (
            id SERIAL PRIMARY KEY,
            round_id VARCHAR(50) UNIQUE,
            crash_point FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_round(round_id: str, crash_point: float):
    """
    Inserts a new round into the DB if not exists.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rounds (round_id, crash_point)
        VALUES (%s, %s)
        ON CONFLICT (round_id) DO NOTHING;
    """, (round_id, crash_point))
    conn.commit()
    cur.close()
    conn.close()

def get_latest_rounds(limit: int = 1000):
    """
    Returns the most recent N rounds ordered by timestamp DESC.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT crash_point FROM rounds ORDER BY timestamp DESC LIMIT %s;", (limit,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [row["crash_point"] for row in data]

def get_all_rounds():
    """
    Returns all rounds in the DB for full retraining.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT crash_point FROM rounds ORDER BY timestamp ASC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [row["crash_point"] for row in data]
