# Task model representing an individual task within a project
class Task:
    def __init__(self, task_id, description, status="Pending"):
        self._task_id = task_id
        self._description = description
        self._status = status

    @property
    def task_id(self):
        return self._task_id

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def to_dict(self):
        return {
            "task_id": self._task_id,
            "description": self._description,
            "status": self._status
        }
