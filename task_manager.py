# task_manager.py
from tasks import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self, loader):
        self.tasks = loader()

    def add_task(self, title, due_date, priority="Medium"):
        task = Task(title, due_date, priority)
        self.tasks.append(task)

    def delete_task(self, title):
        self.tasks = [t for t in self.tasks if t.title != title]
