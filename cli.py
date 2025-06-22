from tool_utils.google_calendar import create_event, list_events_for_date, update_event, delete_event
from tool_utils.notion_notes import create_note, get_notes, update_note, delete_note
from tool_utils.weather import get_weather


# =======================
# 🗓️ Google Calendar Tests
# =======================

def test_calendar():
    print("\n🧪 Testing Google Calendar integration...")

    # 1. Create an event
    created_id = create_event(
        title="Test: MCP Calendar Integration",
        start_iso="2025-06-22T09:00:00",
        end_iso="2025-06-22T10:00:00",
        location="Virtual",
        description="Morning test run for assistant integration"
    )
    print(f"✅ Event created with ID: {created_id}")

    # 2. List all events on the date
    test_date = "2025-06-22"
    events = list_events_for_date(test_date)
    print(f"\n📅 Events on {test_date}:")
    for event in events:
        summary = event.get("summary", "(no title)")
        start = event["start"].get("dateTime", "N/A")
        print(f"- {summary} at {start} [ID: {event['id']}]")

    # 3. Ask to update the event
    do_update = input(f"\n✏️ Do you want to update the created event? (y/n): ").lower()
    if do_update == "y":
        update_event(created_id, summary="✅ UPDATED: MCP Calendar Event", description="Updated via CLI test")
        print(f"✅ Event updated: {created_id}")
    else:
        print("⏭️ Skipped event update.")

    # 4. Ask to delete the event
    do_delete = input("\n🗑️ Do you want to delete the created event? (y/n): ").lower()
    if do_delete == "y":
        delete_event(created_id)
        print(f"✅ Event deleted: {created_id}")
    else:
        print("⏭️ Skipped deletion.")


# =======================
# 📝 Notion Notes Tests
# =======================

def test_notion_notes():
    print("\n🧪 Testing Notion Notes integration...")

    # 1. Create a note
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
            print("⏭️ Skipped note update.")

    # 4. Ask to delete the last note
    if len(notes) > 1:
        last_note = notes[-1]
        do_delete = input(f"\n🗑️ Do you want to delete the last note ('{last_note['title']}')? (y/n): ").lower()
        if do_delete == "y":
            delete_note(last_note["id"])
            print(f"✅ Deleted note ID: {last_note['id']}")
        else:
            print("⏭️ Skipped note deletion.")


# =======================
# 🌤️ Weather API Test
# =======================

def test_weather():
    print("\n🧪 Testing Weather API...")
    city = "Delhi"
    weather_report = get_weather(city)
    print(f"\n🌍 Weather in {city}:\n{weather_report}")


# =======================
# 🧪 Run All Tests
# =======================

if __name__ == "__main__":
    test_calendar()
    test_notion_notes()
    test_weather()
