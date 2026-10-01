# Lab 5 – Test Automation Framework & Self-Healing Locators

**STATUS: scaffold only – NOT executed.** The environment I worked in has no browser, no Docker and cannot download Playwright/Selenium drivers, so steps 4 and 6-9 (running the suite, locator drift, Healenium) have **not been run** and there are no screenshots/results. Do not submit this lab until you have run it yourself; the commands are below. The Flask server itself was verified (add / list / mark-done via Flask's test client).

The repo is a CLI app, so `webapp/server.py` adds a tiny web UI (the "sample web application"). Selenium is used because Healenium heals Selenium WebDriver tests.

## What is here
| Item | File |
|---|---|
| Web UI | `webapp/server.py` |
| Page Object (all locators in one class) | `labs/lab-5/pages/task_page.py` |
| Five data-driven tests (one per CSV row) | `labs/lab-5/test_ui.py`, data in `labs/lab-5/data/tasks.csv` |

## Run it (PowerShell)
```powershell
pip install flask selenium pytest
python -m webapp.server            # terminal 1 -> http://127.0.0.1:5000
pytest labs/lab-5/test_ui.py -v    # terminal 2 – baseline: 5 pass (needs Chrome installed; Selenium 4 fetches the driver)
```
Note: the in-memory task list persists between tests while the server runs, so restart the server before each full run.

## Healenium (steps 5, 8)
Follow the official self-hosted setup (`docker-compose up` from the Healenium "healenium-web" repo), then:
```powershell
$env:HEALENIUM_URL = "http://localhost:8085"   # proxy URL from the compose file
pytest labs/lab-5/test_ui.py -v
```
## Locator drift (steps 6-7)
1. In `webapp/server.py` rename `id="add-btn"` to `id="add-button"`; restart the server.
2. Run **without** `HEALENIUM_URL`: all 5 tests should fail with `NoSuchElementException` for `add-btn`. Save the output as the "before" failure report.
3. Run **with** Healenium: check the dashboard/logs for the healing decision, record how many of the 5 tests healed, and whether it chose the right element.

Reflection prompt: renamed ids/classes are usually healable; changed semantics (button removed, flow reordered) still need a human.
