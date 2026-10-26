"""Web front-end for the task manager, used for Lab 8 (visual regression + accessibility) and Lab 9 (exploratory testing).

  python -m webapp.sample_site                      -> http://127.0.0.1:5001   (original page)

Switches (environment variables, read at start-up):
  LAYOUT_CHANGE=1     small deliberate CSS change for the visual-regression step
  A11Y_FIX=lang,alt   comma list of accessibility fixes to apply: lang, alt, label, button, contrast  (or "all")

The page deliberately ships WITH accessibility problems (no lang attribute, image without alt text,
inputs without labels, an icon-only button with no name, low-contrast text) so the Lab 8 scan has something to find.
"""
import os
from flask import Flask, redirect, render_template_string, request
from app.tasks import add_task, complete_task, get_pending_tasks

LOGO = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48'><rect width='48' height='48' rx='8' fill='%231f6feb'/><text x='24' y='32' font-size='24' text-anchor='middle' fill='white'>T</text></svg>"

PAGE = """<!doctype html>
<html{% if fix.lang %} lang="en"{% endif %}>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Task Manager</title>
<style>
  body { font-family: Arial, sans-serif; margin: 0; background: #ffffff; color: #222; }
  .wrap { margin: 0 {{ '48px' if layout_change else '16px' }}; max-width: 720px; }
  h1 { font-size: {{ '34px' if layout_change else '28px' }}; }
  .muted { color: {{ '#595959' if fix.contrast else '#aaaaaa' }}; }
  input { padding: 8px; margin: 4px 0; }
  button { padding: 8px 14px; background: {{ '#b3261e' if layout_change else '#1f6feb' }}; color: #fff; border: 0; border-radius: 4px; }
  li { margin: 6px 0; }
</style></head>
<body>
<div class="wrap">
  <img src="{{ logo }}" {% if fix.alt %}alt="Task Manager logo"{% endif %} width="48" height="48">
  <h1>Task Manager</h1>
  <p class="muted">Add tasks and mark them done.</p>
  <form action="/add" method="post">
    {% if fix.label %}<label for="title">Title</label><br>{% endif %}
    <input id="title" name="title" placeholder="Title"><br>
    {% if fix.label %}<label for="priority">Priority</label><br>{% endif %}
    <input id="priority" name="priority" value="1"><br>
    <button type="submit">Add task</button>
    <button type="button" id="clear-btn"{% if fix.button %} aria-label="Clear form"{% endif %}><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="#fff" stroke-width="2"/></svg></button>
  </form>
  <p id="pending-count">Pending: {{ pending }}</p>
  <ul id="task-list">
  {% for t in tasks %}<li data-id="{{ t.id }}"><span class="task-title">{{ t.title }}</span> (priority {{ t.priority }})
    {% if t.done %}<em>done</em>{% else %}<a href="/done/{{ t.id }}">Mark done</a>{% endif %}</li>{% endfor %}
  </ul>
</div></body></html>"""


def create_app():
    app = Flask(__name__)
    tasks = []
    fixes = {x.strip() for x in os.environ.get("A11Y_FIX", "").split(",") if x.strip()}
    if "all" in fixes:
        fixes = {"lang", "alt", "label", "button", "contrast"}
    fix = {k: (k in fixes) for k in ("lang", "alt", "label", "button", "contrast")}
    layout_change = os.environ.get("LAYOUT_CHANGE") == "1"

    @app.get("/")
    def index():
        return render_template_string(PAGE, tasks=tasks, pending=len(get_pending_tasks(tasks)),
                                      fix=fix, layout_change=layout_change, logo=LOGO)

    @app.post("/add")
    def add():
        add_task(tasks, request.form["title"], int(request.form.get("priority", 1)))
        return redirect("/")

    @app.get("/reset")
    def reset():
        tasks.clear()   # test helper: gives every UI test a clean slate
        return redirect("/")

    @app.get("/done/<int:task_id>")
    def done(task_id):
        complete_task(tasks, task_id)
        return redirect("/")

    return app


if __name__ == "__main__":
    create_app().run(port=5001)
