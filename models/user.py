from services import storage_service

class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def projects(self):
        db = storage_service.load_all_data()
        return [p for p in db.get("projects", []) if p.get("owner_name", "").lower() == self._name.lower()]

    def to_dict(self):
        return {"name": self._name}