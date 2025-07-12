"""
test_agent.py
Tests for the MCP agent.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from mcp.agent import MCPAgent
from mcp.memory import get_briefing, get_incomplete_todos

@pytest.fixture
def mock_tools():
    with patch('mcp.tools.get_calendar_events') as mock_calendar, \
         patch('mcp.tools.get_notes') as mock_notes, \
         patch('mcp.tools.get_weather') as mock_weather:
        
        mock_calendar.return_value = [
            {"title": "Test Meeting", "time": "10:00", "duration": "1h"}
        ]
        mock_notes.return_value = ["Yesterday's test note"]
        mock_weather.return_value = {
            "temperature": 20,
            "condition": "sunny"
        }
        
        yield {
            "calendar": mock_calendar,
            "notes": mock_notes,
            "weather": mock_weather
        }

@pytest.fixture
def agent():
    return MCPAgent(location="Test City")

def test_get_context(agent, mock_tools):
    context = agent._get_context()
    
    assert "calendar_events" in context
    assert "yesterday_notes" in context
    assert "weather" in context
    assert "date" in context
    assert context["date"] == datetime.now().strftime("%Y-%m-%d")

def test_extract_todos(agent):
    test_summary = """
    Morning Briefing:
    
    TODO: Call John
    - [ ] Send email
    Regular text
    TODO: Review document
    """
    
    todos = agent._extract_todos(test_summary)
    assert len(todos) == 3
    assert "Call John" in todos
    assert "Send email" in todos
    assert "Review document" in todos

@pytest.mark.integration
def test_run_morning_briefing(agent):
    briefing = agent.run_morning_briefing()
    assert briefing is not None
    assert isinstance(briefing, str)
    
    # Check if briefing was stored
    stored_briefing = get_briefing(datetime.now().strftime("%Y-%m-%d"))
    assert stored_briefing == briefing

def test_complete_todo(agent):
    # First store a todo
    today = datetime.now().strftime("%Y-%m-%d")
    from mcp.memory import store_todo
    
    store_todo(today, "Test todo")
    todos = get_incomplete_todos(today)
    assert len(todos) > 0
    
    # Complete the todo
    todo_id = todos[0][0]
    agent.complete_todo(todo_id)
    
    # Verify it's completed
    updated_todos = get_incomplete_todos(today)
    assert len(updated_todos) == len(todos) - 1
