"""
conftest.py
Shared pytest fixtures and test data setup.
"""

import pytest
from datetime import datetime, timedelta

from mcp.memory import store_todo, store_briefing
from tool_utils.google_calendar import create_event
from tool_utils.notion_notes import create_note
from mcp.agent import MCPAgent

@pytest.fixture
def sample_calendar_events():
    """Create and return sample calendar events."""
    today = datetime.now()
    
    events = [
        {
            "title": "Team Standup",
            "start": today.replace(hour=10, minute=0),
            "end": today.replace(hour=10, minute=30),
            "location": "Google Meet",
            "description": "Daily team sync meeting"
        },
        {
            "title": "Lunch with Client",
            "start": today.replace(hour=13, minute=0),
            "end": today.replace(hour=14, minute=0),
            "location": "Cafe Downtown",
            "description": "Project discussion over lunch"
        },
        {
            "title": "Product Workshop",
            "start": today.replace(hour=15, minute=0),
            "end": today.replace(hour=17, minute=0),
            "location": "Conference Room A",
            "description": "Q3 product planning session"
        }
    ]
    
    for event in events:
        create_event(
            event["title"],
            event["start"].isoformat(),
            event["end"].isoformat(),
            event["location"],
            event["description"]
        )
    
    return events

@pytest.fixture
def sample_notes():
    """Create and return sample notes."""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    notes = [
        {
            "content": '''
# Team Meeting Notes

Key points discussed:
- Project timeline review
- New feature requests
- Team capacity planning

Action items:
- Update sprint board
- Schedule design review
- Follow up with DevOps team
            ''',
            "title": f"Meeting Notes - {yesterday}",
            "tags": ["meeting", "team"]
        },
        {
            "content": '''
# Project Ideas

## Features to Consider
1. User authentication improvements
2. Performance optimization
3. Mobile responsiveness

## Technical Debt
- Update dependencies
- Refactor legacy code
- Improve test coverage
            ''',
            "title": "Project Brainstorming",
            "tags": ["ideas", "planning"]
        }
    ]
    
    for note in notes:
        create_note(
            content=note["content"],
            title=note["title"],
            tags=note["tags"]
        )
    
    return notes

@pytest.fixture
def sample_todos():
    """Create and return sample todos."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    todos = [
        "Review pull requests from team",
        "Prepare presentation for tomorrow",
        "Update project documentation",
        "Send weekly status report",
        "Schedule one-on-one meetings"
    ]
    
    for todo in todos:
        store_todo(today, todo)
    
    return todos

@pytest.fixture
def sample_briefing():
    """Create and return a sample briefing."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    briefing = f'''# Morning Briefing - {today}

## Weather
🌤️ Partly cloudy, 22°C

## Today's Schedule
- 10:00 AM - Team Standup
- 1:00 PM - Lunch with Client
- 3:00 PM - Product Workshop

## Yesterday's Notes
- Team meeting discussed project timeline and new features
- Action items identified for sprint planning

## Tasks for Today
- Review pull requests
- Prepare presentation
- Update documentation
- Send status report
- Schedule meetings

Have a productive day! 🚀
    '''
    
    store_briefing(today, briefing)
    return briefing

@pytest.fixture
def mock_tools():
    """Mock external tools for testing."""
    with pytest.MonkeyPatch() as mp:
        mp.setattr('mcp.tools.get_calendar_events', lambda *args: [
            {"title": "Test Meeting", "time": "10:00", "duration": "1h"}
        ])
        mp.setattr('mcp.tools.get_notes', lambda *args: ["Yesterday's test note"])
        mp.setattr('mcp.tools.get_weather', lambda *args: {
            "temperature": 20,
            "condition": "sunny"
        })
        yield

@pytest.fixture
def agent():
    """Create a test agent instance."""
    return MCPAgent(location="Test City")
