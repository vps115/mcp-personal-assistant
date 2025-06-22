import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/notes.db")

def init_notes_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
        ''')
        conn.commit()

def add_note(content: str):
    now = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO notes (content, timestamp) VALUES (?, ?);', (content, now))
        conn.commit()

def get_notes_on(date: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT * FROM notes
            WHERE DATE(timestamp) = ?;
        ''', (date,))
        return cursor.fetchall()

def update_note(note_id: int, new_content: str):
    now = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            UPDATE notes
            SET content = ?, timestamp = ?
            WHERE id = ?;
        ''', (new_content, now, note_id))
        conn.commit()

def delete_note(note_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM notes WHERE id = ?;', (note_id,))
        conn.commit()
