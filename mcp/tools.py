"""
tools.py
Core tool functions for calendar, notes, and weather integration.
"""

from tool_utils.google_calendar import get_calendar_events as gc_get_calendar_events
from tool_utils.notion_notes import get_notes as nn_get_notes
from tool_utils.weather import get_weather as w_get_weather

# Calendar tool stub
def get_calendar_events(start_date, end_date):
    """
    Fetch calendar events between start_date and end_date.
    Args:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
    Returns:
        list: List of event dicts
    """
    # TODO: Connect to Google Calendar integration
    return gc_get_calendar_events(start_date, end_date)

# Create calendar event
def create_calendar_event(title, start_iso, end_iso, location=None, description=None):
    """
    Create a new calendar event.
    Args:
        title (str): Event title
        start_iso (str): ISO datetime string
        end_iso (str): ISO datetime string
        location (str, optional): Event location
        description (str, optional): Event description
    Returns:
        str: Event ID
    """
    from tool_utils.google_calendar import create_event
    return create_event(title, start_iso, end_iso, location, description)

# Update calendar event
def update_calendar_event(event_id, **kwargs):
    """
    Update an existing calendar event.
    Args:
        event_id (str): Event ID
        kwargs: Fields to update
    Returns:
        dict: Updated event
    """
    from tool_utils.google_calendar import update_event
    return update_event(event_id, **kwargs)

# Delete calendar event
def delete_calendar_event(event_id):
    """
    Delete a calendar event.
    Args:
        event_id (str): Event ID
    Returns:
        None
    """
    from tool_utils.google_calendar import delete_event
    return delete_event(event_id)

# Notes tool stub
def get_notes(from_date):
    """
    Fetch notes from a given date.
    Args:
        from_date (str): 'YYYY-MM-DD'
    Returns:
        list: List of note dicts
    """
    # TODO: Connect to Notion Notes integration
    return nn_get_notes(from_date)

# Create note
def create_note(content, title="Untitled", tags=None):
    """
    Create a new note.
    Args:
        content (str): Note content
        title (str, optional): Note title
        tags (list, optional): List of tags
    Returns:
        str: Note ID
    """
    if tags is None:
        tags = []
    from tool_utils.notion_notes import create_note
    return create_note(content, title, tags)

# Update note
def update_note(note_id, new_content=None, new_title=None):
    """
    Update an existing note.
    Args:
        note_id (str): Note ID
        new_content (str, optional): New content
        new_title (str, optional): New title
    Returns:
        None
    """
    from tool_utils.notion_notes import update_note
    return update_note(note_id, new_content, new_title)

# Delete note
def delete_note(note_id):
    """
    Delete a note.
    Args:
        note_id (str): Note ID
    Returns:
        None
    """
    from tool_utils.notion_notes import delete_note
    return delete_note(note_id)

# Weather tool stub
def get_weather(location):
    """
    Fetch weather info for a location.
    Args:
        location (str): City or region name
    Returns:
        dict: Weather data
    """
    # TODO: Connect to weather API integration
    return w_get_weather(location)