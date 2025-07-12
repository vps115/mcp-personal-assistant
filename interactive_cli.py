"""
Interactive CLI for the MCP Agent.
Implements the Model Context Protocol (MCP) for a personal assistant.
"""
from datetime import datetime
import sys
from typing import Dict, List, Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from mcp import tools
from mcp.agent import MCPAgent
from mcp.memory import get_incomplete_todos, complete_todo, store_todo
from mcp.instructions import get_general_prompt
from groq_api import generate_response

console = Console()

class MCPToolServer:
    """Base class for MCP-compliant tool servers."""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.resources = {}
        self.error_state = False
        
    def register_tool(self, tool_name: str, tool_func, description: str):
        """Register a tool with the server."""
        self.tools[tool_name] = {
            "function": tool_func,
            "description": description
        }
    
    def register_resource(self, resource_name: str, resource_func, description: str):
        """Register a resource with the server."""
        self.resources[resource_name] = {
            "function": resource_func,
            "description": description
        }
    
    def call_tool(self, tool_name: str, **params):
        """Execute a registered tool."""
        try:
            if tool_name in self.tools:
                result = self.tools[tool_name]["function"](**params)
                self.error_state = False
                return result
            raise ValueError(f"Tool {tool_name} not found")
        except Exception as e:
            self.error_state = True
            console.print(f"[yellow]Warning: Error in {self.name} server tool {tool_name}: {str(e)}[/yellow]")
            return None
    
    def get_resource(self, resource_name: str, **params):
        """Get a registered resource."""
        try:
            if resource_name in self.resources:
                result = self.resources[resource_name]["function"](**params)
                self.error_state = False
                return result
            raise ValueError(f"Resource {resource_name} not found")
        except Exception as e:
            self.error_state = True
            console.print(f"[yellow]Warning: Error in {self.name} server resource {resource_name}: {str(e)}[/yellow]")
            return None

class CalendarServer(MCPToolServer):
    """MCP server for calendar operations."""
    
    def __init__(self):
        super().__init__("calendar")
        self.register_tool("create_event", tools.create_calendar_event, 
            "Create a calendar event with title, start time, end time, and optional location/description")
        self.register_tool("list_events", tools.get_calendar_events,
            "List calendar events for a given date range")
        self.register_tool("update_event", tools.update_calendar_event,
            "Update an existing calendar event")
        self.register_tool("delete_event", tools.delete_calendar_event,
            "Delete a calendar event")

class NotesServer(MCPToolServer):
    """MCP server for note operations."""
    
    def __init__(self):
        super().__init__("notes")
        self.register_tool("create_note", tools.create_note,
            "Create a new note with content, title, and optional tags")
        self.register_tool("get_notes", tools.get_notes,
            "Get notes from a specific date")
        self.register_tool("update_note", tools.update_note,
            "Update an existing note")
        self.register_tool("delete_note", tools.delete_note,
            "Delete a note")

class WeatherServer(MCPToolServer):
    """MCP server for weather operations."""
    
    def __init__(self, location="New York"):
        super().__init__("weather")
        self.location = location
        self.register_resource("current_weather", lambda: tools.get_weather(self.location),
            f"Get current weather for {self.location}")

class TodoServer(MCPToolServer):
    """MCP server for todo operations."""
    
    def __init__(self):
        super().__init__("todos")
        self.register_tool("add_todo", store_todo,
            "Add a new todo item")
        self.register_tool("complete_todo", complete_todo,
            "Mark a todo as complete")
        self.register_resource("incomplete_todos", get_incomplete_todos,
            "Get list of incomplete todos")

class InteractiveMCPAgent:
    """
    MCP-compliant interactive agent that acts as the client/host.
    Implements the Model Context Protocol for tool and resource management.
    """
    
    def __init__(self):
        self.agent = MCPAgent(location="New York")
        self.conversation_history = []
        
        # Initialize MCP servers
        self.location = "New York"  # Could make this configurable
        self.servers = {
            "calendar": CalendarServer(),
            "notes": NotesServer(),
            "weather": WeatherServer(location=self.location),
            "todos": TodoServer()
        }
        
        # Initialize context with defaults
        self.context = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "servers": list(self.servers.keys()),
            "weather": "Weather information unavailable",
            "calendar_events": [],
            "notes": [],
            "todos": []
        }
    
    def _update_context(self):
        """Update context from all registered MCP servers."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.context["date"] = today
        
        # Get resources from each server
        # Weather
        weather = self.servers["weather"].get_resource("current_weather")
        if weather is not None:
            self.context["weather"] = weather
            
        # Calendar
        calendar = self.servers["calendar"].call_tool("list_events", start_date=today)
        if calendar is not None:
            self.context["calendar_events"] = calendar
            
        # Notes
        notes = self.servers["notes"].call_tool("get_notes", from_date=today)
        if notes is not None:
            self.context["notes"] = notes
            
        # Todos
        todos = self.servers["todos"].get_resource("incomplete_todos", date=today)
        if todos is not None:
            self.context["todos"] = todos
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input using MCP protocol."""
        self._update_context()
        
        # Generate capability information
        capabilities = {}
        for server_name, server in self.servers.items():
            capabilities[server_name] = {
                "status": "available" if not server.error_state else "error"
            }
            if server.tools:
                capabilities[server_name]["tools"] = {
                    name: info["description"] for name, info in server.tools.items()
                }
            if server.resources:
                capabilities[server_name]["resources"] = {
                    name: info["description"] for name, info in server.resources.items()
                }
                
        # Update context with capabilities
        self.context["capabilities"] = capabilities
        
        # Add user input to context
        self.context["user_input"] = user_input
        
        # Handle different types of queries
        if user_input.lower() in ['what can you do', 'help', 'capabilities', 'what are your tools']:
            response = self.agent.get_capabilities()
        
        # Handle weather queries
        elif any(word in user_input.lower() for word in ['weather', 'temperature', 'forecast']):
            # Extract location if provided
            import re
            location_match = re.search(r'(?:in|at|for)\s+([A-Za-z\s]+)(?:\?|$)', user_input)
            if location_match:
                location = location_match.group(1).strip()
                response = self.agent.get_weather(location)
            else:
                response = self.agent.get_weather()
        
        # Handle all other queries
        else:
            prompt = get_general_prompt()
            response = generate_response(prompt, self.context)
            
        return response

    def run(self):
        """Main conversation loop."""
        try:
            # Start with morning briefing
            console.print("[bold blue]🤖 MCP Assistant[/bold blue]")
            console.print("\nGenerating your morning briefing...")
            briefing = self.agent.run_morning_briefing()
            console.print(Markdown(briefing))

            # Main conversation loop
            while True:
                user_input = Prompt.ask("\nHow can I help you?")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("\n[yellow]Goodbye! Have a great day![/yellow]")
                    break

                # Process input and generate response
                response = self.process_user_input(user_input)
                self.conversation_history.append({
                    "user": user_input,
                    "assistant": response
                })
                
                # Display response
                console.print()  # Print blank line
                console.print(Markdown(response))

        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            import traceback
            console.print(traceback.format_exc())

def main():
    """Run the MCP-compliant interactive agent."""
    agent = InteractiveMCPAgent()
    agent.run()

if __name__ == "__main__":
    main()
