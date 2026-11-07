import argparse
from services import storage_service
from services.ai_client import AIClient
from utils import formatters
from models.user import User
from models.project import Project
from models.task import Task
#  ENTRY POINT FOR THE CLI APPLICATION
def main():
    #  Initialize the argument parser and define subcommands
    parser = argparse.ArgumentParser(description="Project Management CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list", help="List all projects")

    user_parser = subparsers.add_parser("create-user", help="Create a new user")
    user_parser.add_argument("--name", required=True, help="Name of the user")

    create_parser = subparsers.add_parser("create-project", help="Create a new project")
    create_parser.add_argument("--title", required=True, help="Title of the project")
    create_parser.add_argument("--desc", required=True, help="Description")
    create_parser.add_argument("--due", required=True, help="Due date (YYYY-MM-DD)")
    create_parser.add_argument("--user", required=True, help="Name of the user creating this project")

    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("--project-id", required=True, type=int, help="Project ID target")
    task_parser.add_argument("--desc", required=True, help="Task description")
    task_parser.add_argument("--status", required=False, choices=["Pending", "In Progress", "Complete"], help="Initial status for the task")

    update_task_parser = subparsers.add_parser("update-task", help="Update the status of a specific task")
    update_task_parser.add_argument("--project-id", required=True, type=int, help="Project ID target")
    update_task_parser.add_argument("--task-id", required=True, type=int, help="Task ID target")
    update_task_parser.add_argument("--status", required=True, choices=["Pending", "In Progress", "Complete"], help="New status for the task")

    ai_parser = subparsers.add_parser("analyze", help="Get an AI status analysis of a project")
    ai_parser.add_argument("--project-id", required=True, type=int, help="Project ID to analyze")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    #  Load the current state of the database into memory
    db = storage_service.load_all_data()
    #  Handle the 'create-user' command
    if args.command == "create-user":
        if not args.name.strip():
            print("Error: User name cannot be empty.")
            return
        if any(u["name"].lower() == args.name.lower() for u in db["users"]):
            print(f"Error: User '{args.name}' already exists.")
            return

        new_user = User(name=args.name)
        db["users"].append(new_user.to_dict())
        storage_service.save_all_data(db)
        formatters.print_success(f"User '{args.name}' created successfully!")
    #  Handle the 'create-project' command
    elif args.command == "create-project":
        if not args.title.strip():
            print("Error: Project title cannot be empty.")
            return
        if not args.desc.strip():
            print("Error: Project description cannot be empty.")
            return
        user_dict = next((u for u in db["users"] if u["name"].lower() == args.user.lower()), None)
        if not user_dict:
            print(f"Error: User '{args.user}' does not exist.")
            return

        new_project = Project(title=args.title, description=args.desc, due_date=args.due)
        
        # Triggers custom .setter wrappers!
        new_project.project_id = len(db["projects"]) + 1
        new_project.owner_name = user_dict["name"]

        db["projects"].append(new_project.to_dict())
        storage_service.save_all_data(db)
        formatters.print_success(f"Project '{new_project.title}' assigned to {new_project.owner_name}!")

    #  Handle the 'add-task' and 'analyze' commands
    elif args.command == "add-task" or args.command == "analyze":
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        project_obj = Project(
            title=project_dict["title"],
            description=project_dict.get("description", ""),
            due_date=project_dict.get("due_date", "")
        )
        # Sets historical parameters through setters smoothly
        project_obj.project_id = project_dict["project_id"]
        project_obj.owner_name = project_dict.get("owner_name")
        project_obj.created_at = project_dict.get("created_at")
        project_obj.tasks = [Task(t["task_id"], t["description"], t["status"]) for t in project_dict.get("tasks", [])]

        if args.command == "add-task":
            if not args.desc.strip():
                print("Error: Task description cannot be empty.")
                return
            if not args.status:
                args.status = "Pending"
            if args.status not in ["Pending", "In Progress", "Complete"]:
                print("Error: Invalid task status.")
                return
            if not args.project_id:
                print("Error: Project ID must be specified.")
                return
            new_task_id = len(project_obj.tasks) + 1
            new_task = Task(task_id=new_task_id, description=args.desc, status=args.status or "Pending")
            project_obj.tasks.append(new_task)

            project_dict["tasks"] = [t.to_dict() for t in project_obj.tasks]
            storage_service.save_all_data(db)
            formatters.print_success(f"Added task to Project ID {args.project_id}!")

        elif args.command == "analyze":
            if not args.project_id:
                print("Error: Project ID must be specified for analysis.")
                return
            print("Talking to local AI model...")
            ai_client = AIClient()
            summary = ai_client.generate_project_summary(project_obj)
            formatters.print_ai_summary(project_obj.title, summary)
    #  Handle the 'update-task' command
    elif args.command == "update-task":
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        task_dict = next((t for t in project_dict.get("tasks", []) if t["task_id"] == args.task_id), None)
        if not task_dict:
            print(f"Error: Task with ID {args.task_id} not found in Project ID {args.project_id}.")
            return

        task_dict["status"] = args.status
        storage_service.save_all_data(db)
        formatters.print_success(f"Updated status of Task ID {args.task_id} in Project ID {args.project_id} to '{args.status}'!")

    elif args.command == "list":
        formatters.print_projects_table(db["projects"])

if __name__ == "__main__":
    main()
