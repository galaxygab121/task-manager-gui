# main.py
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from playsound import playsound
from datetime import datetime, timedelta
from ics import Calendar, Event
import json
import os
from file_utils import load_tasks, save_tasks
from task_manager import TaskManager
from tasks import Task

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager 🗂️")
        self.root.geometry("700x600")

        self.is_dark_mode = False

        self.manager = TaskManager()
        self.manager.load_tasks(load_tasks)

        self.style = ttk.Style()
        self.set_theme()

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filtered_tasks)

        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_var, width=50).pack(side=tk.LEFT)

        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=5)
        self.task_entry = tk.Entry(entry_frame, width=35)
        self.task_entry.grid(row=0, column=0, padx=5)

        self.due_entry = DateEntry(entry_frame, width=12, background='lightpink', foreground='black', date_pattern='yyyy-mm-dd')
        self.due_entry.grid(row=0, column=1, padx=5)

        self.priority_box = ttk.Combobox(entry_frame, values=["Low", "Medium", "High"], width=10)
        self.priority_box.set("Medium")
        self.priority_box.grid(row=0, column=2, padx=5)

        tk.Button(entry_frame, text="Add", command=self.add_task).grid(row=0, column=3, padx=5)
        tk.Button(entry_frame, text="Toggle 🌙/☀️", command=self.toggle_theme).grid(row=0, column=4)

        self.tree = ttk.Treeview(root, columns=("Due", "Priority"), show="headings", selectmode="browse")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(expand=True, fill="both", pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack()
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Export to iCal", command=self.export_ics).pack(side=tk.LEFT, padx=10)

        self.refresh_tasks()
        self.schedule_reminders()

    def set_theme(self):
        if self.is_dark_mode:
            self.style.configure(".", background="#1a001a", foreground="hotpink", fieldbackground="#2b0033")
            self.root.configure(bg="#1a001a")
        else:
            self.style.configure(".", background="lavenderblush", foreground="black", fieldbackground="white")
            self.root.configure(bg="lavenderblush")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.set_theme()

    def add_task(self):
        title = self.task_entry.get()
        due_date = self.due_entry.get_date()
        priority = self.priority_box.get()

        if not title.strip():
            messagebox.showwarning("Warning", "Please enter a task title.")
            return

        self.manager.add_task(title, due_date.strftime("%Y-%m-%d"), priority)
        save_tasks(self.manager.tasks)
        playsound("ding.mp3")
        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            task_title = self.tree.item(selected[0])['values'][0]
            self.manager.delete_task(task_title)
            save_tasks(self.manager.tasks)
            self.refresh_tasks()

    def refresh_tasks(self):
        self.tree.delete(*self.tree.get_children())
        for task in sorted(self.manager.tasks, key=lambda x: x.due_date):
            self.tree.insert("", tk.END, values=(task.title, task.due_date, task.priority))

    def update_filtered_tasks(self, *_):
        keyword = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for task in self.manager.tasks:
            if keyword in task.title.lower():
                self.tree.insert("", tk.END, values=(task.title, task.due_date, task.priority))

    def schedule_reminders(self):
        now = datetime.now()
        for task in self.manager.tasks:
            due = datetime.strptime(task.due_date, "%Y-%m-%d")
            if 0 < (due - now).total_seconds() < 86400:
                messagebox.showinfo("Reminder", f"⏰ '{task.title}' is due tomorrow!")

    def export_ics(self):
        cal = Calendar()
        for task in self.manager.tasks:
            event = Event()
            event.name = task.title
            event.begin = task.due_date
            event.description = f"Priority: {task.priority}"
            cal.events.add(event)
        with open("tasks.ics", "w") as f:
            f.writelines(cal)
        messagebox.showinfo("Exported", "Tasks exported to tasks.ics")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
