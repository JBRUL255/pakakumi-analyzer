# pakakumi_analyzer/app/db.py

import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "pakakumi.db")


def init_db():
    """Initialize the database with rounds table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_number INTEGER UNIQUE,
            cashout REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Context manager for safe DB connections."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def insert_round(round_number: int, cashout: float):
    """Insert a new round result into the database."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO rounds (round_number, cashout) VALUES (?, ?)",
            (round_number, cashout),
        )
        conn.commit()


def get_all_rounds():
    """Retrieve all past rounds' cashout multipliers."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT cashout FROM rounds ORDER BY round_number ASC")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def get_latest_rounds(limit: int = 50):
    """Retrieve the most recent rounds."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT cashout FROM rounds ORDER BY round_number DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
    # Return newest first, consistent order
    return [r[0] for r in reversed(rows)]


def get_round_count():
    """Return total number of rounds stored."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM rounds")
        return cur.fetchone()[0]
