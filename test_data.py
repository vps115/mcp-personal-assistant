"""
test_data.py
Script to populate test data for the personal assistant.
"""

from datetime import datetime, timedelta
import sys

from mcp.memory import store_todo, store_briefing
from tool_utils.google_calendar import create_event
from tool_utils.notion_notes import create_note

def create_sample_calendar_events():
    """Create sample calendar events for today."""
    print("Creating sample calendar events...")
    today = datetime.now()
    
    # Morning standup
    start_time = today.replace(hour=10, minute=0)
    end_time = start_time + timedelta(minutes=30)
    create_event(
        "Team Standup",
        start_time.isoformat(),
        end_time.isoformat(),
        location="Google Meet",
        description="Daily team sync meeting"
    )
    print("✓ Created standup event")
    
    # Lunch meeting
    start_time = today.replace(hour=13, minute=0)
    end_time = start_time + timedelta(hours=1)
    create_event(
        "Lunch with Client",
        start_time.isoformat(),
        end_time.isoformat(),
        location="Cafe Downtown",
        description="Project discussion over lunch"
    )
    print("✓ Created lunch event")
    
    # Afternoon workshop
    start_time = today.replace(hour=15, minute=0)
    end_time = start_time + timedelta(hours=2)
    create_event(
        "Product Workshop",
        start_time.isoformat(),
        end_time.isoformat(),
        location="Conference Room A",
        description="Q3 product planning session"
    )
    print("✓ Created workshop event")

def create_sample_notes():
    """Create sample notes."""
    print("\nCreating sample notes...")
    
    # Yesterday's meeting notes
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    create_note(
        content="""
# Team Meeting Notes

Key points discussed:
- Project timeline review
- New feature requests
- Team capacity planning

Action items:
- Update sprint board
- Schedule design review
- Follow up with DevOps team
        """,
        title=f"Meeting Notes - {yesterday}",
        tags=["meeting", "team"]
    )
    print("✓ Created yesterday's meeting notes")
    
    # Project ideas
    create_note(
        content="""
# Project Ideas

## Features to Consider
1. User authentication improvements
2. Performance optimization
3. Mobile responsiveness

## Technical Debt
- Update dependencies
- Refactor legacy code
- Improve test coverage
        """,
        title="Project Brainstorming",
        tags=["ideas", "planning"]
    )
    print("✓ Created project ideas note")

def create_sample_todos():
    """Create sample todos in the memory DB."""
    print("\nCreating sample todos...")
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
        print(f"✓ Created todo: {todo}")

def create_sample_briefing():
    """Create a sample briefing in memory."""
    print("\nCreating sample briefing...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    briefing = f"""# Morning Briefing - {today}

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
    """
    
    store_briefing(today, briefing)
    print("✓ Created sample briefing")

def main():
    """Run all sample data creation."""
    try:
        print("=== Creating Sample Data ===\n")
        create_sample_calendar_events()
        create_sample_notes()
        create_sample_todos()
        create_sample_briefing()
        print("\n✨ All sample data created successfully!")
        
    except Exception as e:
        print(f"\n❌ Error creating sample data: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
