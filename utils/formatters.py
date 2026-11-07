from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def print_success(message):
    console.print(f"[bold green]✔ Success:[/bold green] {message}")

def print_ai_summary(title, summary_text):
    console.print(Panel(summary_text, title=f"🤖 AI Insight: {title}", border_style="cyan"))

def print_projects_table(projects_list):
    if not projects_list:
        console.print("[bold yellow]No active projects found.[/bold yellow]")
        return

    for p in projects_list:

        project_table = Table(title="Project")
        project_table.add_column("Project ID", style="yellow", justify="center")
        project_table.add_column("Title", style="bold white")
        project_table.add_column("Owner", style="cyan")
        project_table.add_column("Created", style="white")
        project_table.add_column("Due-Date", style="yellow")

        # Clean up the ISO timestamp to show just the YYYY-MM-DD portion for readability
        clean_date = p['created_at'].split('T')[0] if 'T' in p['created_at'] else p['created_at']
        
        project_table.add_row(
            str(p['project_id']),
            p['title'], 
            p.get('owner_name', 'Unassigned'), 
            clean_date, 
            p['due_date']
        )
        
        console.print(project_table)

        tasks = p.get("tasks", [])
        if tasks:
            # Shift the task sub-table slightly to the right using padding spaces for clean visual hierarchy
            task_table = Table(title="  ↳ Project Tasks", title_style="dim italic text", border_style="dim")
            task_table.add_column("  Task ID", style="yellow", justify="center")
            task_table.add_column("Description", style="white")
            task_table.add_column("Status", style="green")

            for t in tasks:
                # Add status coloring dynamically based on keyword flags
                status_str = t['status']
                if status_str == "Complete":
                    status_display = f"[bold green]{status_str}[/bold green]"
                elif status_str == "In Progress":
                    status_display = f"[bold yellow]{status_str}[/bold yellow]"
                else:
                    status_display = f"[bold dim]{status_str}[/bold dim]"

                task_table.add_row(f"  {t['task_id']}", t['description'], status_display)
            
            console.print(task_table)
        else:
            console.print("  [dim italic]↳ No tasks added to this project yet.[/dim italic]")
        
        # Print a subtle dividing line break space between distinct project segments
        console.print("\n" + "─" * 60 + "\n")