"""
agent.py
Main MCP agent logic for the personal assistant.
Implements Model-Context Protocol (MCP) with Instructions, Tools, Memory, and Chain-of-Tools.
"""

from datetime import datetime, timedelta
import logging
import os
from typing import Dict, List, Optional

from . import tools
from . import memory
from . import instructions
from groq_api import generate_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MCPAgent:
    def __init__(self, location: str = "New York"):
        """Initialize the MCP agent with default location for weather."""
        self.location = location
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        logger.info(f"Initialized MCPAgent with location: {location}")

    def _get_context(self) -> Dict:
        """
        Gather context from all tools for the briefing.
        Returns:
            dict: Combined context from all tools
        """
        logger.debug("Gathering context from tools...")
        
        try:
            # Get today's calendar events
            calendar_events = tools.get_calendar_events(
                start_date=self.today,
                end_date=self.today
            )
            logger.debug(f"Retrieved {len(calendar_events)} calendar events")

            # Get yesterday's notes
            yesterday_notes = tools.get_notes(from_date=self.yesterday)
            logger.debug(f"Retrieved {len(yesterday_notes)} notes from yesterday")

            # Get weather info
            weather_info = tools.get_weather(self.location)
            logger.debug("Retrieved weather information")

            # Get incomplete todos
            incomplete_todos = memory.get_incomplete_todos(self.yesterday)
            logger.debug(f"Retrieved {len(incomplete_todos)} incomplete todos")

            context = {
                "calendar_events": calendar_events,
                "yesterday_notes": yesterday_notes,
                "weather": weather_info,
                "incomplete_todos": incomplete_todos,
                "date": self.today
            }
            
            logger.info("Successfully gathered all context")
            return context
            
        except Exception as e:
            logger.error(f"Error gathering context: {str(e)}")
            raise

    def _extract_todos(self, summary: str) -> List[str]:
        """
        Extract todo items from the briefing summary.
        Args:
            summary (str): Generated briefing summary
        Returns:
            list: Extracted todo items
        """
        # TODO: Use LLM to extract actionable items from the summary
        # For now, looking for lines starting with "TODO:" or "- [ ]"
        todos = []
        for line in summary.split('\n'):
            line = line.strip()
            if line.startswith('TODO:') or line.startswith('- [ ]'):
                todos.append(line.replace('TODO:', '').replace('- [ ]', '').strip())
        return todos

    def run_morning_briefing(self) -> str:
        """
        Run the morning briefing chain-of-tools flow.
        Returns:
            str: Generated briefing summary
        """
        # 1. Instructions: Get the prompt template
        prompt = instructions.get_morning_briefing_prompt()

        # 2. Tools: Gather context from all tools
        context = self._get_context()

        # 3. Generate briefing using LLM
        briefing = generate_response(
            prompt=prompt,
            context=context
        )

        # 4. Memory: Store briefing and extract todos
        memory.store_briefing(self.today, briefing)
        
        # Extract and store todos
        todos = self._extract_todos(briefing)
        for todo in todos:
            memory.store_todo(self.today, todo)

        logger.info("Morning briefing completed and stored")
        return briefing

    def complete_todo(self, todo_id: int) -> None:
        """
        Mark a todo item as completed.
        Args:
            todo_id (int): ID of the todo item
        """
        memory.complete_todo(todo_id)
        logger.info(f"Marked todo ID {todo_id} as completed")

    def get_previous_briefing(self, date: Optional[str] = None) -> Optional[str]:
        """
        Retrieve a previous briefing.
        Args:
            date (str, optional): Date in YYYY-MM-DD format. Defaults to yesterday.
        Returns:
            str: Briefing summary if found, None otherwise
        """
        date = date or self.yesterday
        briefing = memory.get_briefing(date)
        if briefing:
            logger.info(f"Retrieved briefing for {date}")
        else:
            logger.info(f"No briefing found for {date}")
        return briefing
