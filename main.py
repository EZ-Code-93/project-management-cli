import argparse
from services import storage_service
from services.ai_client import AIClient
from utils import formatters
from models.user import User
from models.project import Project
from models.task import Task

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: create-user --name <str>
    user_parser = subparsers.add_parser("create-user", help="Create a new user")
    user_parser.add_argument("--name", required=True, help="Name of the user")

    # Command: create-project --title <str> --desc <str> --due <str> --user <str>
    create_parser = subparsers.add_parser("create-project", help="Create a new project")
    create_parser.add_argument("--title", required=True, help="Title of the project")
    create_parser.add_argument("--desc", required=True, help="Description")
    create_parser.add_argument("--due", required=True, help="Due date (YYYY-MM-DD)")
    create_parser.add_argument("--user", required=True, help="Name of the user creating this project")

    task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    task_parser.add_argument("--project-id", required=True, type=int, help="Project ID target")
    task_parser.add_argument("--desc", required=True, help="Task description")

    # Command: list
    subparsers.add_parser("list", help="List all projects")

    # Command: analyze --project-id <id>
    ai_parser = subparsers.add_parser("analyze", help="Get an AI status analysis of a project")
    ai_parser.add_argument("--project-id", required=True, type=int, help="Project ID to analyze")

    args = parser.parse_args()
    db = storage_service.load_all_data()

    if args.command == "create-user":
        # Check if user already exists
        if any(u["name"].lower() == args.name.lower() for u in db["users"]):
            print(f"Error: User '{args.name}' already exists.")
            return

        new_user = User(name=args.name)
        db["users"].append(new_user.to_dict())
        storage_service.save_all_data(db)
        formatters.print_success(f"User '{args.name}' created successfully!")

    elif args.command == "create-project":
        # 1. Enforce that the user must exist first
        user_dict = next((u for u in db["users"] if u["name"].lower() == args.user.lower()), None)
        if not user_dict:
            print(f"Error: User '{args.user}' does not exist. Please create the user first using 'create-user'.")
            return

        # 2. Instantiate the clean project
        new_project = Project(title=args.title, description=args.desc, due_date=args.due)
        
        # 3. Assign structural fields dynamically
        new_project.project_id = len(db["projects"]) + 1
        new_project.owner_name = user_dict["name"] # Assigned via their exact tracked name!

        # 4. Save to global projects list and update the user's personal project tracking array
        db["projects"].append(new_project.to_dict())
        
        storage_service.save_all_data(db)
        formatters.print_success(f"Project '{args.title}' created and assigned to {new_project.owner_name}!")

    elif args.command == "add-task":
        # 1. Locate the targeted project dictionary from the global master list
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        # 2. Reconstruct the Project object from saved database values
        project_obj = Project(
            title=project_dict["title"],
            description=project_dict.get("description", ""),
            due_date=project_dict.get("due_date", "")
        )
        # Re-apply tracking variables that aren't inside __init__
        project_obj.project_id = project_dict["project_id"]
        project_obj.owner_name = project_dict.get("owner_name")
        project_obj.created_at = project_dict.get("created_at")
        
        # Hydrate existing tasks back into clean Task instances
        project_obj.tasks = [
            Task(t["task_id"], t["description"], t["status"]) 
            for t in project_dict.get("tasks", [])
        ]

        # 3. Instantiate and append the new task instance natively
        new_task_id = len(project_obj.tasks) + 1
        new_task = Task(task_id=new_task_id, description=args.desc)
        project_obj.tasks.append(new_task)

        # 4. Serialize the updated task list back to our master dictionary reference
        project_dict["tasks"] = [t.to_dict() for t in project_obj.tasks]
        
        # 5. Commit structural modifications straight back to the JSON file
        storage_service.save_all_data(db)
        formatters.print_success(f"Added task '{args.desc}' to Project ID {args.project_id} successfully!")


    elif args.command == "list":
        formatters.print_projects_table(db["projects"])

    elif args.command == "analyze":
        # 1. Locate the target project dictionary from the global master list
        project_dict = next((p for p in db["projects"] if p["project_id"] == args.project_id), None)
        if not project_dict:
            print(f"Error: Project with ID {args.project_id} not found.")
            return

        # 2. Reconstruct the clean Project object signature
        project_obj = Project(
            title=project_dict["title"],
            description=project_dict.get("description", ""),
            due_date=project_dict.get("due_date", "")
        )
        project_obj.project_id = project_dict["project_id"]
        project_obj.owner_name = project_dict.get("owner_name")
        project_obj.created_at = project_dict.get("created_at")
        
        # Hydrate nested task maps into clean Task instances for the AI prompt context
        project_obj.tasks = [
            Task(t["task_id"], t["description"], t["status"]) 
            for t in project_dict.get("tasks", [])
        ]

        # 3. Fire off the structured prompt data to Ollama
        print("Talking to local AI model...")
        ai_client = AIClient()
        summary = ai_client.generate_project_summary(project_obj)
        
        # 4. Display the results utilizing your rich layout panels
        formatters.print_ai_summary(project_obj.title, summary)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
