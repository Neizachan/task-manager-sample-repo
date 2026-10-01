"""Lab 5 - five data-driven UI tests (one per row of data/tasks.csv).

Plain Selenium run:      pytest labs/lab-5/test_ui.py
Through Healenium proxy: set HEALENIUM_URL=http://localhost:8085  (PowerShell: $env:HEALENIUM_URL="http://localhost:8085")
The web app must be running:  python -m webapp.server
"""
import csv, os, pathlib, pytest
from selenium import webdriver
from labs_lab5_pages import TaskPage  # noqa  (see conftest path shim below)

DATA = pathlib.Path(__file__).parent / "data" / "tasks.csv"
ROWS = list(csv.DictReader(open(DATA, encoding="utf-8")))


@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    hub = os.environ.get("HEALENIUM_URL")
    drv = webdriver.Remote(command_executor=hub, options=opts) if hub else webdriver.Chrome(options=opts)
    yield drv
    drv.quit()


@pytest.mark.parametrize("row", ROWS, ids=[r["title"] for r in ROWS])
def test_add_task_shows_in_list(driver, row):
    page = TaskPage(driver, os.environ.get("APP_URL")).open()
    before = len(page.titles())
    page.add_task(row["title"], row["priority"])
    assert row["title"] in page.titles()
    assert len(page.titles()) == before + 1
