# MCP Personal Assistant

A conversational AI assistant built using the Model Context Protocol (MCP) that helps manage your daily tasks, calendar, notes, and provides weather updates.

## Project Structure

```
mcp-personal-assistant/
├── mcp/                      # Core MCP implementation
│   ├── agent.py             # Main agent logic
│   ├── tools.py             # Tool implementations
│   ├── memory.py            # Memory management
│   ├── instructions.py      # Prompt templates
│   └── __init__.py
├── tool_utils/              # External integrations
│   ├── google_calendar.py   # Google Calendar integration
│   ├── notion_notes.py      # Notion Notes integration
│   ├── weather.py           # Weather API integration
│   └── __init__.py
├── tests/                   # Test files
│   ├── test_agent.py       # Agent tests
│   └── test_cli.py         # CLI tests
├── interactive_cli.py       # Main CLI interface
├── groq_api.py             # LLM API wrapper
├── requirements.txt         # Dependencies
├── .env.example            # Environment variables template
└── README.md               # This file

## Features

- 🗣️ Natural Language Interface
- 📅 Google Calendar Integration
- 📝 Notion Notes Integration
- 🌤️ Weather Updates
- ✅ Todo Management
- 🧠 Contextual Awareness
- 💾 Persistent Storage
  - SQLite database for todos and briefings
  - Automatic data directory management
  - Efficient indexing for better performance

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-personal-assistant.git
cd mcp-personal-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your API keys and credentials:
  - GROQ_API_KEY: LLM API key
  - NOTION_TOKEN: Notion integration token
  - NOTION_DATABASE_ID: Notion database ID
  - OPENWEATHER_API_KEY: OpenWeather API key
  - Set up Google Calendar credentials (see below)

5. Set up Google Calendar:
- Go to Google Cloud Console
- Create a project and enable Google Calendar API
- Create credentials and download as `google_calendar_credentials.json`
- Place in project root

## Usage

Run the interactive CLI:
```bash
python interactive_cli.py
```

The assistant will:
1. Show your morning briefing
2. Accept natural language commands
3. Help manage your tasks, calendar, and notes

Example commands:
- "What's on my calendar today?"
- "Add a note about the meeting"
- "What's the weather like?"
- "Create a todo to follow up with John"

## Data Storage

The application uses SQLite for persistent storage:
- Location: `data/notes.db` (automatically created on first run)
- Tables:
  - `briefings`: Stores daily briefing history
  - `todos`: Manages todo items and their status
- Features:
  - Automatic initialization
  - Performance-optimized indices
  - Automatic data directory creation
  - No manual setup required

## Testing

Run tests:
```bash
python -m pytest tests/
```

## License

MIT License - See LICENSE file for details

