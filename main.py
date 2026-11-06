import argparse
from services import storage_service
from services.ai_client import AIClient
from utils import formatters
from models.project import Project
from models.task import Task

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    subparsers.add_parser("list", help="List all projects")

    # Command: create-project --title <name>
    create_parser = subparsers.add_parser("create-project", help="Create a new project")
    create_parser.add_argument("--title", required=True, help="Title of the project")

    # Command: add-task --project-id <id> --desc <text>
    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("--project-id", required=True, type=int, help="Project ID target")
    task_parser.add_argument("--desc", required=True, help="Task description")

    # Command: analyze --project-id <id>
    ai_parser = subparsers.add_parser("analyze", help="Get an AI status analysis of a project")
    ai_parser.add_argument("--project-id", required=True, type=int, help="Project ID to analyze")

    args = parser.parse_args()

    # 1. Load active snapshot from the database file
    db = storage_service.load_all_data()

    if args.command == "list":
        formatters.print_projects_table(db["projects"])

    elif args.command == "create-project":
        new_id = len(db["projects"]) + 1
        # Instantiate object model
        new_project = Project(project_id=new_id, title=args.title, owner_id=1)
        
        # Add serialized data back to database snapshot
        db["projects"].append(new_project.to_dict())
        storage_service.save_all_data(db)
        formatters.print_success(f"Project '{args.title}' created successfully with ID {new_id}!")

    elif args.command == "add-task":
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        # Reconstruct the project object from dict data to update it natively
        project_obj = Project(project_dict["project_id"], project_dict["title"], project_dict["owner_id"])
        # Load up existing tasks into instances
        project_obj.tasks = [Task(t["task_id"], t["description"], t["status"]) for t in project_dict.get("tasks", [])]

        # Add the new task object
        new_task_id = len(project_obj.tasks) + 1
        new_task = Task(task_id=new_task_id, description=args.desc)
        project_obj.tasks.append(new_task)

        # Re-serialize back to the tracking database dictionary slot
        project_dict["tasks"] = [t.to_dict() for t in project_obj.tasks]
        storage_service.save_all_data(db)
        formatters.print_success(f"Added task '{args.desc}' to Project ID {args.project_id}!")

    elif args.command == "analyze":
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        # Hydrate to object form so the AI module receives a clean native object structure
        project_obj = Project(project_dict["project_id"], project_dict["title"], project_dict["owner_id"])
        project_obj.tasks = [Task(t["task_id"], t["description"], t["status"]) for t in project_dict.get("tasks", [])]

        print("Talking to local AI model...")
        ai_client = AIClient()
        summary = ai_client.generate_project_summary(project_obj)
        formatters.print_ai_summary(project_obj.title, summary)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
