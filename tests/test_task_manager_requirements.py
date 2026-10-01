"""Lab 4 - requirement-based tests. Each test name carries its Test Case ID (see labs/lab-4/rtm.md)."""
import json
import pytest
import app.tasks as tasks_mod
from app.tasks import (add_task, complete_task, get_pending_tasks, average_priority,
                       remove_task, find_task_by_title, save_tasks, load_tasks)
from app.storage import format_task_report


# R1 - adding a task: defaults and unique ids
def test_TC4_01_add_task_defaults():
    t = add_task([], "A")
    assert (t["priority"], t["tags"], t["done"]) == (1, [], False)

def test_TC4_02_add_task_ids_unique_after_removal():
    tasks = []
    for name in "ABC":
        add_task(tasks, name)
    remove_task(tasks, 1)
    add_task(tasks, "D")
    ids = [t["id"] for t in tasks]
    assert len(ids) == len(set(ids)), f"duplicate ids {ids}"

# R2 - completing a task
def test_TC4_03_complete_existing_task():
    tasks = []; add_task(tasks, "A")
    assert complete_task(tasks, 1) is True and tasks[0]["done"] is True

def test_TC4_04_complete_unknown_id_returns_false():
    tasks = []; add_task(tasks, "A")
    assert complete_task(tasks, 99) is False and tasks[0]["done"] is False

# R3 - pending tasks
def test_TC4_05_pending_excludes_done_includes_first():
    tasks = []
    for name in "ABC":
        add_task(tasks, name)
    complete_task(tasks, 2)
    assert [t["title"] for t in get_pending_tasks(tasks)] == ["A", "C"]

# R4 - average priority
def test_TC4_06_average_priority_values_and_empty():
    tasks = []
    add_task(tasks, "A", priority=1); add_task(tasks, "B", priority=4)
    assert average_priority(tasks) == 2.5
    assert average_priority([]) == 0

# R5 - removing a task
def test_TC4_07_remove_task_by_id():
    tasks = []; add_task(tasks, "A"); add_task(tasks, "B")
    remove_task(tasks, 1)
    assert [t["title"] for t in tasks] == ["B"]

# R6 - persistence
def test_TC4_08_save_then_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(tasks_mod, "TASKS_FILE", str(tmp_path / "t.json"))
    tasks = []; add_task(tasks, "A", tags=["x"])
    save_tasks(tasks)
    assert load_tasks() == tasks

def test_TC4_09_load_missing_file_gives_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(tasks_mod, "TASKS_FILE", str(tmp_path / "nope.json"))
    assert load_tasks() == []

# R7 - report
def test_TC4_10_report_lists_every_task():
    tasks = []; add_task(tasks, "Write report"); add_task(tasks, "Test")
    assert format_task_report(tasks) == "Task #1: Write report\nTask #2: Test"

# R8 - lookup by title
def test_TC4_11_find_by_title_first_match_or_none():
    tasks = []; add_task(tasks, "A"); add_task(tasks, "A")
    assert find_task_by_title(tasks, "A")["id"] == 1
    assert find_task_by_title(tasks, "Z") is None
