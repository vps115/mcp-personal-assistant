"""
memory.py
SQLite-backed memory for storing and retrieving morning briefings and incomplete tasks.
"""
import sqlite3
import os
from datetime import datetime

# Set up database path
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DB_PATH = os.path.join(DB_DIR, 'notes.db')

# Ensure DB and table exist
def init_db():
    """Initialize the SQLite database and create required tables."""
    # Create data directory if it doesn't exist
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create briefings table
    c.execute('''CREATE TABLE IF NOT EXISTS briefings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create todos table
    c.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        todo TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )''')
    
    # Create indices for better performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_briefings_date ON briefings(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_todos_date ON todos(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed)')
    
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
