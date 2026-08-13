
import sqlite3
from pathlib import Path

DB = Path("bot/database/cache.db")

def init_cache():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS question_cache(
            topic TEXT,
            count INTEGER,
            questions TEXT,
            PRIMARY KEY(topic, count)
        )
        """
    )
    conn.commit()
    conn.close()
