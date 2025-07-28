# tasks.py
class Task:
    def __init__(self, title, due_date, priority="Medium"):
        self.title = title
        self.due_date = due_date
        self.priority = priority

    def to_dict(self):
        return {"title": self.title, "due_date": self.due_date, "priority": self.priority}

    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["due_date"], data.get("priority", "Medium"))
