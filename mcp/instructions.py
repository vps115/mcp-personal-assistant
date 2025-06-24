class ToolSchema:
    """
    Defines the structure and usage of each tool available to the agent.
    """

    @staticmethod
    def get_manifest() -> str:
        return """
You have access to the following tools. Use exactly one tool per query.

Tools:

1. calendar
  - Description: Manage calendar events
  - Actions:
      • create_event(title: str, start_iso: str, end_iso: str, location: Optional[str], description: Optional[str])
      • list_events_for_date(date: str)
      • update_event(event_id: str, summary: Optional[str], location: Optional[str], description: Optional[str])
      • delete_event(event_id: str)

2. notes
  - Description: Manage personal notes stored in Notion
  - Actions:
      • create_note(content: str, title: Optional[str], tags: Optional[list[str]])
      • get_notes()
      • update_note(note_id: str, new_content: Optional[str], new_title: Optional[str])
      • delete_note(note_id: str)

3. weather
  - Description: Get current weather in a city
  - Actions:
      • get_weather(city: str)

Respond ONLY with a JSON object of the form:
{
  "tool": "<tool_name>",
  "action": "<action_name>",
  "args": { <dictionary of arguments> }
}
"""


class PromptBuilder:
    """
    Builds LLM-friendly prompts for tool selection from user input.
    """

    def __init__(self, tool_schema: ToolSchema = ToolSchema()):
        self.tool_schema = tool_schema

    def build_tool_selection_prompt(self, user_query: str) -> str:
        """
        Compose a complete prompt instructing the LLM how to choose a tool and parameters.
        """
        return f"""
You are an AI assistant that selects tools and arguments based on user queries.

User query:
'{user_query}'

Instructions:
- Think step-by-step.
- Choose the most appropriate tool.
- Identify the correct action to perform.
- Extract any arguments from the query.
- Only include parameters explicitly stated or safely assumed.
- If no tool fits, return "tool": "none".
- Respond ONLY with a JSON object.

{self.tool_schema.get_manifest()}
"""
