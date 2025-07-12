"""
mcp package
Main MCP (Model Context Protocol) implementation for the personal assistant.
"""

from .agent import MCPAgent
from .tools import (
    get_calendar_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
    get_notes,
    create_note,
    update_note,
    delete_note,
    get_weather
)
from .memory import (
    store_briefing,
    get_briefing,
    store_todo,
    get_incomplete_todos,
    complete_todo
)

__all__ = [
    'MCPAgent',
    'get_calendar_events',
    'create_calendar_event',
    'update_calendar_event',
    'delete_calendar_event',
    'get_notes',
    'create_note',
    'update_note',
    'delete_note',
    'get_weather',
    'store_briefing',
    'get_briefing',
    'store_todo',
    'get_incomplete_todos',
    'complete_todo'
]
