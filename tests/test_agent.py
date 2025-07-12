"""
test_agent.py
Unit and integration tests for the MCP agent.
"""

import pytest
from datetime import datetime, timedelta

from mcp.agent import MCPAgent
from mcp.memory import get_briefing, get_incomplete_todos, store_todo

# Unit Tests with Mocks

def test_get_context(agent, mock_tools):
    """Test context gathering with mocked tools."""

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
    """Test todo completion functionality."""
    today = datetime.now().strftime("%Y-%m-%d")
    store_todo(today, "Test todo")
    todos = get_incomplete_todos(today)
    assert len(todos) > 0
    
    todo_id = todos[0][0]
    agent.complete_todo(todo_id)
    
    updated_todos = get_incomplete_todos(today)
    assert len(updated_todos) == len(todos) - 1

# Integration Tests with Real Data

@pytest.mark.integration
def test_full_workflow(agent, sample_calendar_events, sample_notes, sample_todos):
    """Test the full agent workflow with sample data."""
    # 1. Generate morning briefing
    briefing = agent.run_morning_briefing()
    assert briefing is not None
    assert isinstance(briefing, str)
    
    # 2. Verify briefing was stored
    stored_briefing = get_briefing(datetime.now().strftime("%Y-%m-%d"))
    assert stored_briefing == briefing
    
    # 3. Check todos were extracted
    todos = agent._extract_todos(briefing)
    assert len(todos) > 0
    
    # 4. Test weather query
    weather = agent.get_weather("Test City")
    assert weather is not None
    assert "Temperature" in weather

@pytest.mark.integration
def test_data_persistence(agent, sample_todos):
    """Test data persistence across agent restarts."""
    # 1. Get initial todos
    today = datetime.now().strftime("%Y-%m-%d")
    initial_todos = get_incomplete_todos(today)
    assert len(initial_todos) > 0
    
    # 2. Complete a todo
    todo_id = initial_todos[0][0]
    agent.complete_todo(todo_id)
    
    # 3. Create new agent instance
    new_agent = MCPAgent(location="Test City")
    
    # 4. Verify todo state persists
    updated_todos = get_incomplete_todos(today)
    assert len(updated_todos) == len(initial_todos) - 1
