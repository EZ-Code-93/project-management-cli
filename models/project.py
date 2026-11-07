from datetime import datetime
from models.task import Task

# Project model representing a project with tasks, owner, and metadata
class Project:
    def __init__(self, title, description, due_date):
        self._title = title
        self._description = description
        self._due_date = due_date
        self._created_at = datetime.now().isoformat()
        
        self._project_id = None
        self._owner_name = None
        self.tasks = []  # Public reference to internal instance lists

    # --- Getters & Setters for Core Fields ---
    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def due_date(self):
        return self._due_date

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    # --- Getters & Setters for Structural IDs ---
    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, value):
        self._project_id = value

    @property
    def owner_name(self):
        return self._owner_name

    @owner_name.setter
    def owner_name(self, value):
        self._owner_name = value

    def to_dict(self):
        return {
            "project_id": self._project_id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "created_at": self._created_at,
            "owner_name": self._owner_name,
            "tasks": [task.to_dict() for task in self.tasks]
        }