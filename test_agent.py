"""
test_agent.py
Simple script to test the MCPAgent functionality directly.
"""
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown

from mcp import MCPAgent
from mcp.memory import get_incomplete_todos

console = Console()

def test_agent():
    """Test the core agent functionality."""
    try:
        # Initialize agent
        console.print("\n[blue]Initializing MCPAgent...[/blue]")
        agent = MCPAgent(location="New York")
        
        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Test getting context
        console.print("\n[blue]Testing context gathering...[/blue]")
        context = agent._get_context()
        console.print("Context retrieved:", style="green")
        console.print(context)
        
        # 2. Test generating briefing
        console.print("\n[blue]Generating morning briefing...[/blue]")
        briefing = agent.run_morning_briefing()
        console.print("\n[green]Briefing generated:[/green]")
        console.print(Markdown(briefing))
        
        # 3. Test todo extraction and retrieval
        console.print("\n[blue]Checking todos...[/blue]")
        todos = get_incomplete_todos(today)
        if todos:
            console.print("\n[green]Found todos:[/green]")
            for todo_id, text in todos:
                console.print(f"- [{todo_id}] {text}")
        else:
            console.print("[yellow]No todos found[/yellow]")
            
    except Exception as e:
        import traceback
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("[red]Traceback:[/red]")
        console.print(traceback.format_exc())

if __name__ == "__main__":
    console.print("[bold blue]=== Testing MCP Agent ===\n")
    test_agent()
