# Testing Google Calendar integration

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


print("Testing Google Calendar integration...")

# Create an event
created_id = test_create()

# List all events on that date
test_list("2025-06-22")

# Delete the event
delete_prompt = input("\nDelete created event? (y/n): ")
if delete_prompt.lower() == "y":
    test_delete(created_id)

# Testing Notion Notes integration
from tool_utils.notion_notes import create_note, get_notes, update_note, delete_note

print("Testing Google Calendar integration...")
# 1. Create a new note
create_note(
    "This is a test note from MCP Assistant",
    "Assistant Startup Log",
    tags=["assistant", "test"]
)
print("✅ Created note")

# 2. List all notes
notes = get_notes()
print("\n📓 Current Notes:")
for i, note in enumerate(notes):
    print(f"{i + 1}. {note['title']}: {note['content']} (Date: {note['date']})")

# 3. Ask to update the first note
if notes:
    first_note = notes[0]
    do_update = input(f"\n✏️ Do you want to update the first note ('{first_note['title']}')? (y/n): ").lower()
    if do_update == "y":
        update_note(
            note_id=first_note["id"],
            new_content="🚀 Updated content from CLI test",
            new_title=f"UPDATED: {first_note['title']}"
        )
        print(f"✅ Updated note ID: {first_note['id']}")
    else:
        print("⏭️ Skipped update.")

# 4. Ask to delete the last note
if len(notes) > 1:
    last_note = notes[-1]
    do_delete = input(f"\n🗑️ Do you want to delete the last note ('{last_note['title']}')? (y/n): ").lower()
    if do_delete == "y":
        delete_note(last_note["id"])
        print(f"✅ Deleted note ID: {last_note['id']}")
    else:
        print("⏭️ Skipped deletion.")

