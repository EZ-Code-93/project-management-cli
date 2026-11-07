from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def print_success(message):
    console.print(f"[bold green]✔ Success:[/bold green] {message}")

def print_ai_summary(title, summary_text):
    console.print(Panel(summary_text, title=f"🤖 AI Insight: {title}", border_style="cyan"))

def print_projects_table(projects_list):
    table = Table(title="All Active Projects")
    table.add_column("Project ID", style="yellow", justify="center")
    table.add_column("Title", style="bold white")
    table.add_column("Owner", style="cyan")
    table.add_column("Created", style="white")
    table.add_column("Due-Date", style="yellow")

    for p in projects_list:
        # Clean up the ISO timestamp to show just the YYYY-MM-DD portion for readability
        clean_date = p['created_at'].split('T')[0] if 'T' in p['created_at'] else p['created_at']
        
        table.add_row(
            str(p['project_id']),
            p['title'], 
            p.get('owner_name', 'Unassigned'), 
            clean_date, 
            p['due_date']
        )
        
    console.print(table)
