import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "project_data.json")

def load_all_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "projects": []}
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": [], "projects": []}

def save_all_data(db_snapshot):
    # Ensure data folder exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as file:
        json.dump(db_snapshot, file, indent=4)


