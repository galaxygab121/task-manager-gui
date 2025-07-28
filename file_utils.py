# file_utils.py
import json
from tasks import Task

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return [Task.from_dict(t) for t in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)
