"""
Simple CLI test for the MCP Agent functionality.
Tests each component individually and then combines them.
"""
from datetime import datetime
import sys
from rich.console import Console
from rich.markdown import Markdown

from mcp import tools
from mcp.agent import MCPAgent
from mcp.memory import get_incomplete_todos

console = Console()

def test_individual_components():
    """Test each integration separately."""
    console.print("\n[blue]Testing individual components:[/blue]")
    
    # 1. Test Weather
    console.print("\n[yellow]Testing Weather API...[/yellow]")
    try:
        weather = tools.get_weather("New York")
        console.print("[green]✓ Weather API working[/green]")
        console.print(f"Current weather in New York: {weather}")
    except Exception as e:
        console.print(f"[red]✗ Weather API error: {str(e)}[/red]")

    # 2. Test Notion Notes
    console.print("\n[yellow]Testing Notion integration...[/yellow]")
    try:
        notes = tools.get_notes(datetime.now().strftime("%Y-%m-%d"))
        console.print("[green]✓ Notion API working[/green]")
        console.print(f"Found {len(notes)} notes")
    except Exception as e:
        console.print(f"[red]✗ Notion API error: {str(e)}[/red]")

    # 3. Test Calendar
    console.print("\n[yellow]Testing Google Calendar integration...[/yellow]")
    try:
        events = tools.get_calendar_events(datetime.now().strftime("%Y-%m-%d"))
        console.print("[green]✓ Calendar API working[/green]")
        console.print(f"Found {len(events)} events")
    except Exception as e:
        console.print(f"[red]✗ Calendar API error: {str(e)}[/red]")

    # 4. Test LLM (Groq)
    console.print("\n[yellow]Testing Groq LLM...[/yellow]")
    try:
        from groq_api import generate_response
        response = generate_response(
            prompt="Say 'LLM test successful' if you can read this.",
            context={}
        )
        console.print("[green]✓ Groq LLM working[/green]")
        console.print(f"LLM Response: {response}")
    except Exception as e:
        console.print(f"[red]✗ Groq LLM error: {str(e)}[/red]")

def test_full_briefing():
    """Test the full morning briefing functionality."""
    console.print("\n[blue]Testing full morning briefing:[/blue]")
    
    try:
        agent = MCPAgent(location="New York")
        briefing = agent.run_morning_briefing()
        
        console.print("\n[green]Morning Briefing Generated:[/green]")
        console.print(Markdown(briefing))
        
        # Check for todos
        todos = get_incomplete_todos(datetime.now().strftime("%Y-%m-%d"))
        if todos:
            console.print("\n[green]Found todos:[/green]")
            for todo_id, text in todos:
                console.print(f"- [{todo_id}] {text}")
    except Exception as e:
        console.print(f"\n[red]Error in full briefing: {str(e)}[/red]")
        import traceback
        console.print(traceback.format_exc())

if __name__ == "__main__":
    console.print("[bold blue]MCP Agent CLI Test[/bold blue]")
    
    # First test individual components
    test_individual_components()
    
    # Then test full briefing
    console.print("\n[bold blue]Press Enter to test full briefing generation...[/bold blue]")
    input()
    test_full_briefing()
