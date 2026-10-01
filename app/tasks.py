
"""Task management core logic."""
import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from disk, returning an empty list if no file exists."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return []
#fixed the above code snippet where if os.path.exists(TASKS_FILE): was changed to include the encoding parameter in the open function to ensure proper reading of the file

def save_tasks(tasks):
    """Persist tasks to disk."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)


def add_task(tasks, title, priority=1, tags=None):
    """Create a new task and append it to the task list."""
    if tags is None:
        tags = []
    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "priority": priority,
        "tags": tags,
        "done": False,
    }
    tasks.append(task)
    return task
#fixed the above code snippet wher tags=[] was changed to tags=None and added a check to set it to an empty list if None

def complete_task(tasks, task_id):
    """Mark a task as done by id."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def get_pending_tasks(tasks):
    """Return all tasks that are not yet done."""
    return [task for task in tasks if not task["done"]]


def average_priority(tasks):
    """Return the average priority across all tasks."""
    if not tasks:
        return 0
    total = sum(task["priority"] for task in tasks)
    return total / len(tasks)


def find_task_by_title(tasks, title):
    """Return the first task matching the given title."""
    for task in tasks:
        if task["title"] == title:
            return task


def remove_task(tasks, task_id):
    """Remove a task by id."""
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            del tasks[i]
            break


def calculate_discount(price, is_premium):
    """Apply a loyalty discount for premium users."""
    if is_premium:
        return price * 0.8
    return price
#the fix is_premium is already a bolean,so just tests ttruthiness directly and dropped else after return clears pylints no-else-return warning