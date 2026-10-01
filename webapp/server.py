"""Minimal web front-end for the task manager (needed for Lab 5: the repo itself is CLI-only).
Run:  pip install flask  &&  python -m webapp.server     -> http://127.0.0.1:5000
"""
from flask import Flask, redirect, request, render_template_string
from app.tasks import add_task, complete_task, get_pending_tasks

PAGE = """<!doctype html><title>Task Manager</title>
<h1>Task Manager</h1>
<form action="/add" method="post">
  <input id="title-input" name="title" placeholder="Title">
  <input id="priority-input" name="priority" type="number" value="1">
  <button id="add-btn" type="submit">Add</button>
</form>
<p id="pending-count">Pending: {{ pending }}</p>
<ul id="task-list">
{% for t in tasks %}<li class="task-item" data-id="{{ t.id }}">
  <span class="task-title">{{ t.title }}</span> (p{{ t.priority }})
  {% if t.done %}<em class="done-label">done</em>
  {% else %}<a class="done-link" href="/done/{{ t.id }}">Mark done</a>{% endif %}</li>{% endfor %}
</ul>"""

tasks = []
app = Flask(__name__)

@app.get("/")
def index():
    return render_template_string(PAGE, tasks=tasks, pending=len(get_pending_tasks(tasks)))

@app.post("/add")
def add():
    add_task(tasks, request.form["title"], int(request.form.get("priority", 1)))
    return redirect("/")

@app.get("/done/<int:task_id>")
def done(task_id):
    complete_task(tasks, task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000)