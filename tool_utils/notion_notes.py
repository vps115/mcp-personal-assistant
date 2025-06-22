from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DB_ID = os.getenv("NOTION_DATABASE_ID")

def create_note(content: str, title: str = "Untitled", tags: list = []):
    date = datetime.now().date().isoformat()
    
    props = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Content": {"rich_text": [{"text": {"content": content}}]},
    }
    if tags:
        props["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}
    if date:
        props["Date"] = {"date": {"start": date}}

    notion.pages.create(parent={"database_id": DB_ID}, properties=props)

def get_notes():
    results = notion.databases.query(database_id=DB_ID)["results"]
    notes = []
    for page in results:
        props = page["properties"]
        notes.append({
            "id": page["id"],
            "title": props["Title"]["title"][0]["plain_text"] if props["Title"]["title"] else "Untitled",
            "content": props["Content"]["rich_text"][0]["plain_text"] if props["Content"]["rich_text"] else "",
            "date": props.get("Date", {}).get("date", {}).get("start", None)
        })
    return notes

def delete_note(note_id):
    notion.blocks.delete(note_id)

def update_note(note_id, new_content=None, new_title=None):
    updates = {}
    if new_title:
        updates["Title"] = {"title": [{"text": {"content": new_title}}]}
    if new_content:
        updates["Content"] = {"rich_text": [{"text": {"content": new_content}}]}
    today = datetime.now().date().isoformat()
    if today:
        updates["Date"] = {"date": {"start": today}}
    notion.pages.update(page_id=note_id, properties=updates)
