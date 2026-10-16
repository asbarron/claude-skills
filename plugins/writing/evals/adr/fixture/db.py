import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "dev.sqlite3")

SCHEMA = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)"


def connect(path=None):
    conn = sqlite3.connect(path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def add_item(conn, name):
    cur = conn.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    return cur.lastrowid


def list_items(conn):
    return [row["name"] for row in conn.execute("SELECT name FROM items ORDER BY id")]
