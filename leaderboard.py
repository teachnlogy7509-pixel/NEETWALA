
import sqlite3
from pathlib import Path

DB = Path("bot/database/neet_bot.db")

def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_stats(
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            score INTEGER DEFAULT 0,
            tests INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()

def top_users(limit=10):
    init_db()
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT name, score FROM user_stats ORDER BY score DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows
