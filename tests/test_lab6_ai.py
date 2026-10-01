"""Lab 6 - AI-generated unit tests (Claude, prompted with each function's code + docstring; not hand-tuned).
Targets: app.storage.days_until_due, app.storage.build_query, app.cli.main
"""
import json
import pytest
from freezegun import freeze_time

from app.storage import days_until_due, build_query
from app.cli import main


# ---------- days_until_due ----------
@freeze_time("2026-10-01")
def test_days_until_due_future_date():
    assert days_until_due("2026-10-11") == 10


@freeze_time("2026-10-01")
def test_days_until_due_past_date():
    assert days_until_due("2026-09-21") == -10


@freeze_time("2026-10-01")
def test_days_until_due_today():
    assert days_until_due("2026-10-01") == 0


def test_days_until_due_invalid_format_raises():
    with pytest.raises(ValueError):
        days_until_due("10/01/2026")


# ---------- build_query ----------
def test_build_query_basic():
    assert build_query("Write report") == "SELECT * FROM tasks WHERE title = 'Write report'"


def test_build_query_empty_string():
    query = build_query("")
    assert query.startswith("SELECT * FROM tasks")


def test_build_query_contains_title():
    assert "O'Brien" in build_query("O'Brien")


# ---------- main ----------
def test_main_with_no_tasks_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    main()
    out = capsys.readouterr().out
    assert "Loaded 0 tasks" in out


def test_main_with_tasks(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    data = [
        {"id": 1, "title": "A", "priority": 1, "tags": [], "done": False},
        {"id": 2, "title": "B", "priority": 2, "tags": [], "done": True},
    ]
    (tmp_path / "tasks.json").write_text(json.dumps(data))
    main()
    out = capsys.readouterr().out
    assert "Loaded 2 tasks" in out
    assert "Pending tasks: 1" in out
