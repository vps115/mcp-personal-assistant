# cli.py

from tool_utils.google_calendar import create_event, list_events_for_date, delete_event

def test_create():
    event_id = create_event(
        title="Test: MCP Calendar Integration",
        start_iso="2025-06-22T09:00:00",
        end_iso="2025-06-22T10:00:00",
        location="Virtual",
        description="Morning test run for assistant integration"
    )
    print(f"✅ Event created with ID: {event_id}")
    return event_id

def test_list(date: str):
    events = list_events_for_date(date)
    print(f"\n📅 Events on {date}:")
    for event in events:
        summary = event.get("summary", "(no title)")
        start = event["start"].get("dateTime", "N/A")
        print(f"- {summary} at {start} [ID: {event['id']}]")

def test_delete(event_id):
    delete_event(event_id)
    print(f"🗑️ Event deleted: {event_id}")

if __name__ == "__main__":
    print("Testing Google Calendar integration...")

    # Create an event
    created_id = test_create()

    # List all events on that date
    test_list("2025-06-22")

    # Optionally delete the event
    delete_prompt = input("\nDelete created event? (y/n): ")
    if delete_prompt.lower() == "y":
        test_delete(created_id)
