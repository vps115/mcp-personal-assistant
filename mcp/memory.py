"""
memory.py
SQLite-backed memory for storing and retrieving morning briefings and incomplete tasks.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'notes.db')

# Ensure DB and table exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS briefings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        summary TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        todo TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

# Store a morning briefing
def store_briefing(date, summary):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO briefings (date, summary) VALUES (?, ?)', (date, summary))
    conn.commit()
    conn.close()

# Retrieve briefing by date
def get_briefing(date):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT summary FROM briefings WHERE date = ?', (date,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# Store a to-do
def store_todo(date, todo):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO todos (date, todo) VALUES (?, ?)', (date, todo))
    conn.commit()
    conn.close()

# Get incomplete to-dos
def get_incomplete_todos(date):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, todo FROM todos WHERE date = ? AND completed = 0', (date,))
    rows = c.fetchall()
    conn.close()
    return rows

# Mark to-do as completed
def complete_todo(todo_id):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = 1 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
