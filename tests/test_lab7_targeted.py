"""Lab 7 - tests written to kill the mutants that survived the AI-generated suite.

M1  app.cli.main  print(format_task_report(tasks)) -> print(None)   (mutmut: x_main__mutmut_13)
      AI tests only checked 'Loaded N tasks' / 'Pending tasks: N' with `in`, never the report body.
M2  app.storage.days_until_due  re-introducing DEF-003 (datetime.now() with time of day)
      AI tests froze the clock at 00:00, where the buggy and fixed versions agree.
"""
import json
from freezegun import freeze_time
from app.cli import main
from app.storage import days_until_due


def test_m1_main_prints_the_report_body(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "tasks.json").write_text(json.dumps([
        {"id": 1, "title": "Alpha", "priority": 1, "tags": [], "done": False},
        {"id": 2, "title": "Beta", "priority": 2, "tags": [], "done": True},
    ]))
    main()
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["Loaded 2 tasks", "Task #1: Alpha", "Task #2: Beta", "Pending tasks: 1"]


@freeze_time("2026-10-01 10:30:00")
def test_m2_due_today_and_tomorrow_midday():
    assert days_until_due("2026-10-01") == 0
    assert days_until_due("2026-10-02") == 1


@freeze_time("2026-10-01 23:59:59")
def test_m2_due_today_just_before_midnight():
    assert days_until_due("2026-10-01") == 0
