class Task:
    def __init__(self, task_id, description, status="Pending"):
        self.task_id = task_id
        self.description = description
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status
        }
