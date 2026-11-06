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
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="bold white")
    table.add_column("Task Count", justify="right", style="green")

    for p in projects_list:
        table.add_row(str(p['project_id']), p['title'], str(len(p.get('tasks', []))))
        
    console.print(table)