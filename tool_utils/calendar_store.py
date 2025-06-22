import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/calendar.db")

def init_calendar_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                location TEXT,
                desc TEXT
            );
        ''')
        conn.commit()

def add_event(title, start_time, end_time, location=None, desc=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO calendar_events (title, start_time, end_time, location, desc)
            VALUES (?, ?, ?, ?, ?);
        ''', (title, start_time, end_time, location, desc))
        conn.commit()

def get_events_on(date: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT * FROM calendar_events
            WHERE DATE(start_time) = ?;
        ''', (date,))
        return cursor.fetchall()

def update_event(event_id, **kwargs):
    columns = ', '.join(f"{k} = ?" for k in kwargs.keys())
    values = list(kwargs.values())
    values.append(event_id)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(f'''
            UPDATE calendar_events
            SET {columns}
            WHERE id = ?;
        ''', values)
        conn.commit()

def delete_event(event_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM calendar_events WHERE id = ?;', (event_id,))
        conn.commit()
