# mcp-personal-assistant
LLM based Personal Assistant using MCP

---

# 🧠 Smart Personal Assistant (MCP-Based)

## 🪄 Project Overview

This is an AI-powered **smart personal assistant** built using the principles of the **Model Context Protocol (MCP)**. The assistant is designed to provide useful, contextual summaries and reflections by combining:

- **LLM-based reasoning**
- **Structured tools** (e.g., calendar, note fetcher, weather API)
- **Evolving memory** (short- and long-term)
- **Transparent step-wise execution** (Chain-of-Tools logic)

Unlike traditional chatbots, this assistant is **modular, explainable, and session-aware**, offering users real productivity support.

---

## 🎯 Project Goal (v0.1)

Implement a **Morning Briefing Assistant** that:

1. CRUD today's calendar events
2. CRUD notes and Gathers yesterday’s notes
3. Pulls in weather information
4. Summarizes the above in natural language
5. Remembers previous summaries and missed to-dos

---

## 🧱 Current Scope

| Component      | Description |
|----------------|-------------|
| ✅ Instructions | The prompt/goal given to the model: _"Give me a morning briefing"_ |
| ✅ Tools        | - `get_calendar_events(start_date, end_date)`  <br> - `get_notes(from_date)` <br> - *(optional)* `get_weather(location)` |
| ✅ Memory       | Simple in-memory or SQLite-based DB to store:  <br> - Notes <br> - Past briefings <br> - Incomplete tasks |
| 🧠 Model        | llama-3.1-8b-instant (for now) |
| 🧪 Interface    | CLI to test flows; optional FastAPI frontend in later stages |

---

## 🔧 Tech Stack

| Area          | Tool |
|---------------|------|
| Language Model | llama-3.1-8b-instant |
| Tool Logic     | Python functions for notes/calendar integration |
| Orchestration  | Custom Chain-of-Tools logic (MCP-like) |
| Memory         | SQLite |
| API Layer      | FastAPI (optional; later stage) |
| Dev Interface  | CLI (Week 1 MVP) |

---

## 📁 Project Structure

```
personal\_assistant/
├── mcp/
│   ├── tools.py         # Calendar, notes, weather tool interfaces
│   ├── instructions.py  # Prompt templates
│   ├── memory.py        # Memory module (SQLite or in-memory)
│   ├── agent.py         # Chain-of-Tools orchestration
├── api/                 # (Optional) FastAPI app
│   └── main.py
├── data/                # Persistent notes, calendar events
│   └── notes.db
└── README.md
```

---

## 🚀 Phase 1: MVP Checklist

- [x] Define goal prompt for “Morning Briefing”
- [ ] Build simple `get_calendar_events()` stub
- [ ] Build `get_notes()` tool (read from file or DB)
- [ ] Chain tool outputs into LLM summary
- [ ] Store and retrieve briefing history
- [ ] Create CLI to run `briefing()` agent

---

## 🧩 Future Extensions (Post-MVP)

- Add tool: `get_emails_summary()`
- Add tool: `get_tasks_from_yesterday()`
- Add journaling support: “How are you feeling today?”
- Create reflection summary: “How was your week?”
- Web UI via FastAPI or Streamlit
- MCP-compliant logging of all tool calls, LLM steps, and memory diffs

---

## 🧠 MCP Alignment

| MCP Component | Implementation |
|---------------|----------------|
| **Instructions** | Defined prompts for goals like “briefing”, “reflect”, etc. |
| **Tools**        | Each function (calendar, notes, weather) is a callable module |
| **Memory**       | Long-term: SQLite or ChromaDB <br> Short-term: session context |
| **Chain-of-Tools** | Sequential reasoning using tools + LLM for synthesis |
| **Transparency** | Each step (input/output) is visible and loggable |

