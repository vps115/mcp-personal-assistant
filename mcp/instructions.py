"""
instructions.py
Prompt templates and LLM goals for the MCP agent.
"""

def get_morning_briefing_prompt() -> str:
    """
    Returns the prompt template for generating morning briefings.
    """
    return """You are a helpful personal assistant generating a morning briefing.
    
Context:
- Today's date: {context[date]}
- Weather: {context[weather]}
- Calendar events today: {context[calendar_events]}
- Notes from yesterday: {context[yesterday_notes]}
- Incomplete tasks: {context[incomplete_todos]}

Please provide a natural, concise briefing that:
1. Summarizes today's weather and how it might affect plans
2. Lists today's calendar events chronologically
3. Highlights key points from yesterday's notes
4. Reminds about any incomplete tasks
5. Suggests any necessary preparations or actions (mark these with TODO:)

Format the response in a clear, organized way using markdown headings."""
