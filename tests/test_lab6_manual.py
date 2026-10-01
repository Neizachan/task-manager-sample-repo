"""Lab 6 - manually written tests (no AI) for days_until_due, build_query, cli.main."""
import json
import pytest
from freezegun import freeze_time

from app.storage import days_until_due, build_query
from app.cli import main

BUG_TIME = pytest.mark.xfail(strict=True, reason="DEFECT DEF-003: days_until_due ignores that now() has a time of day")
BUG_SQL = pytest.mark.xfail(strict=True, reason="DEFECT DEF-004: build_query does not escape quotes (SQL injection) - to be handled in Lab 12")


# ---------- days_until_due (clock frozen at 10:30, i.e. NOT midnight) ----------
@freeze_time("2026-10-01 10:30:00")
@pytest.mark.parametrize("due, expected", [
    ("2026-10-11", 10),
    ("2026-10-01", 0),      # due today
    ("2026-10-02", 1),      # due tomorrow
    ("2026-09-30", -1),     # due yesterday
    ("2026-09-21", -10),
    ("2027-01-01", 92),     # across a month/year boundary
])
def test_days_until_due_calendar_days(due, expected):
    assert days_until_due(due) == expected


@freeze_time("2028-02-28 23:59:00")
def test_days_until_due_leap_day():
    assert days_until_due("2028-02-29") == 1


@pytest.mark.parametrize("bad", ["", "10/01/2026", "2026-13-01", "2026-02-30", "tomorrow", None])
def test_days_until_due_rejects_bad_input(bad):
    with pytest.raises((ValueError, TypeError)):
        days_until_due(bad)


# ---------- build_query ----------
@pytest.mark.parametrize("title, expected", [
    ("Report", "SELECT * FROM tasks WHERE title = 'Report'"),
    ("", "SELECT * FROM tasks WHERE title = ''"),
    ("two words", "SELECT * FROM tasks WHERE title = 'two words'"),
])
def test_build_query_exact_text(title, expected):
    assert build_query(title) == expected


@BUG_SQL
def test_build_query_escapes_single_quote():
    assert build_query("O'Brien") == "SELECT * FROM tasks WHERE title = 'O''Brien'"


@BUG_SQL
def test_build_query_neutralises_injection_payload():
    assert "OR '1'='1" not in build_query("' OR '1'='1")


def test_build_query_rejects_non_string():
    with pytest.raises(TypeError):
        build_query(None)


# ---------- main ----------
def _run(tmp_path, monkeypatch, capsys, tasks=None):
    monkeypatch.chdir(tmp_path)
    if tasks is not None:
        (tmp_path / "tasks.json").write_text(json.dumps(tasks))
    main()
    return capsys.readouterr().out


def test_main_empty_output_is_exact(tmp_path, monkeypatch, capsys):
    assert _run(tmp_path, monkeypatch, capsys) == "Loaded 0 tasks\n\nPending tasks: 0\n"


def test_main_output_is_exact_with_tasks(tmp_path, monkeypatch, capsys):
    tasks = [
        {"id": 1, "title": "A", "priority": 1, "tags": [], "done": False},
        {"id": 2, "title": "B", "priority": 2, "tags": [], "done": True},
        {"id": 3, "title": "C", "priority": 3, "tags": [], "done": False},
    ]
    out = _run(tmp_path, monkeypatch, capsys, tasks)
    assert out == "Loaded 3 tasks\nTask #1: A\nTask #2: B\nTask #3: C\nPending tasks: 2\n"


def test_main_all_done_reports_zero_pending(tmp_path, monkeypatch, capsys):
    tasks = [{"id": 1, "title": "A", "priority": 1, "tags": [], "done": True}]
    assert _run(tmp_path, monkeypatch, capsys, tasks).endswith("Pending tasks: 0\n")
