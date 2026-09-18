import csv
import io
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.getenv("DATABASE_PATH", "data/knowledge_bot.db"))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language_code TEXT,
                joined_at TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                is_blocked INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                chapter TEXT,
                extracted_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def save_user(user):
    if not user:
        return
    timestamp = now_iso()
    with connect() as connection:
        connection.execute(
            """
            INSERT INTO users(chat_id, username, first_name, last_name, language_code, joined_at, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                language_code=excluded.language_code,
                last_seen=excluded.last_seen,
                is_blocked=0
            """ ,
            (user.id, user.username, user.first_name, user.last_name, user.language_code, timestamp, timestamp),
        )


def list_chat_ids():
    with connect() as connection:
        rows = connection.execute("SELECT chat_id FROM users WHERE is_blocked = 0 ORDER BY last_seen DESC").fetchall()
    return [row["chat_id"] for row in rows]


def mark_blocked(chat_id):
    with connect() as connection:
        connection.execute("UPDATE users SET is_blocked = 1, last_seen = ? WHERE chat_id = ?", (now_iso(), chat_id))


def user_count():
    with connect() as connection:
        return connection.execute("SELECT COUNT(*) FROM users WHERE is_blocked = 0").fetchone()[0]


def recent_users(limit=20):
    with connect() as connection:
        return connection.execute(
            "SELECT chat_id, username, first_name, last_name, last_seen FROM users ORDER BY last_seen DESC LIMIT ?",
            (limit,),
        ).fetchall()


def save_document(chat_id, filename, chapter, extracted_text):
    with connect() as connection:
        connection.execute(
            "INSERT INTO documents(chat_id, filename, chapter, extracted_text, created_at) VALUES (?, ?, ?, ?, ?)",
            (chat_id, filename, chapter, extracted_text, now_iso()),
        )


def latest_document(chat_id):
    with connect() as connection:
        return connection.execute(
            "SELECT filename, chapter, extracted_text, created_at FROM documents WHERE chat_id = ? ORDER BY id DESC LIMIT 1",
            (chat_id,),
        ).fetchone()


def users_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["chat_id", "username", "first_name", "last_name", "last_seen"])
    for row in recent_users(limit=100000):
        writer.writerow([row["chat_id"], row["username"] or "", row["first_name"] or "", row["last_name"] or "", row["last_seen"]])
    return output.getvalue()
