# TODO: Need to add start and end time in calendar events update function

from dotenv import load_dotenv
from ..tool_utils.google_calendar import create_event, list_events_for_date, delete_event, update_event
from ..tool_utils.notion_notes import create_note, get_notes, delete_note, update_note
from ..tool_utils.weather import get_weather
import os


load_dotenv()


class CalendarTool:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']

    def create_event(self, title: str, start_iso: str, end_iso: str, location: str = None, description: str = None) -> str:
        try:
            event_id = create_event(title, start_iso, end_iso, location, description, self.scopes)
            return f"Event created successfully with ID: {event_id}"
        except Exception as e:
            return f"Failed to create event: {e}"

    def list_events(self, date: str) -> str:
        try:
            events = list_events_for_date(date, self.scopes)
            if not events:
                return "No events found for this date."
            return "\n".join([
                f"Event Title: {event.get('summary', '(no title)')}, "
                f"Description: {event.get('description', '(no description)')}, "
                f"Start: {event['start'].get('dateTime', 'N/A')}, "
                f"End: {event['end'].get('dateTime', 'N/A')}, "
                f"Location: {event.get('location', '(no location)')}, "
                f"Event ID: {event['id']}"
                for event in events
            ])
        except Exception as e:
            return f"Failed to list events: {e}"

    def delete_event(self, event_id: str) -> str:
        try:
            delete_event(event_id, self.scopes)
            return f"Event with ID {event_id} deleted successfully."
        except Exception as e:
            return f"Failed to delete event: {e}"

    def update_event(self, event_id: str, **kwargs) -> str:
        try:
            update_event(event_id, self.scopes, **kwargs)
            return f"Event with ID {event_id} updated successfully."
        except Exception as e:
            return f"Failed to update event: {e}"


class NotesTool:
    def __init__(self):
        pass

    def create_note(self, content: str, title: str = "Untitled", tags: list = None) -> str:
        try:
            create_note(content, title, tags or [])
            return "Note created successfully."
        except Exception as e:
            return f"Failed to create note: {e}"

    def get_notes(self) -> str:
        try:
            notes = get_notes()
            if not notes:
                return "No notes found."
            return "\n".join([
                f"Title: {note['title']}, Content: {note['content']}, Date: {note.get('date', 'N/A')}, ID: {note['id']}"
                for note in notes
            ])
        except Exception as e:
            return f"Failed to retrieve notes: {e}"

    def delete_note(self, note_id: str) -> str:
        try:
            delete_note(note_id)
            return f"Note with ID {note_id} deleted successfully."
        except Exception as e:
            return f"Failed to delete note: {e}"

    def update_note(self, note_id: str, new_content: str = None, new_title: str = None) -> str:
        try:
            update_note(note_id, new_content, new_title)
            return f"Note with ID {note_id} updated successfully."
        except Exception as e:
            return f"Failed to update note: {e}"


class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city: str = "Delhi", units: str = "metric") -> str:
        try:
            return get_weather(city, units, self.api_key)
        except Exception as e:
            return f"Failed to fetch weather: {e}"


def get_tools():
    return {
        "calendar": CalendarTool(),
        "notes": NotesTool(),
        "weather": WeatherTool(),
    }