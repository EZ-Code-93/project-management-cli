from models.task import Task

class Project:
    def __init__(self, project_id, title, owner_id):
        self.project_id = project_id
        self.title = title
        self.owner_id = owner_id
        self.tasks = []  # Holds Task instances

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "owner_id": self.owner_id,
            "tasks": [task.to_dict() for task in self.tasks]
        }




'''
class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []
'''