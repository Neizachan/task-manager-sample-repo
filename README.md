# Task Manager (Lab 1 Sample Repository)

A tiny in-memory/file-backed task manager used as the seeded sample project
for Module Lab 1 (Environment Setup & Manual Defect Hunting).

## Setup
```
pip install -r requirements.txt
```

## Run
```
python -m app.cli
```

## Test
```
pytest
```

## Labs 3-7 (COMP 441)
Reports: `labs/lab-3` … `labs/lab-7` (Lab 4 is the Library System RTM; `tests/test_task_manager_requirements.py` is a supplement). Run everything: `python -m pytest tests -q` (59 passed, 9 xfailed = documented open defects).
Mutation testing (Lab 7) needs Linux/WSL: `mutmut run "app.storage.x_days_until_due*" "app.storage.x_build_query*" "app.cli.x_main*"`.
Lab 5 is a scaffold (Page Object + data-driven Selenium tests on the-internet.herokuapp.com + a local mirror for the drift step) that must be executed locally – see `labs/lab-5/README.md`.
