from datetime import datetime
from models.task import Task

class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.created_at = datetime.now().isoformat()
        
        self.project_id = None
        self.owner_name = None  # Will hold the string name of the creator
        self.tasks = []

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "owner_name": self.owner_name,
            "tasks": [task.to_dict() for task in self.tasks]
        }
