"""Lab 5 - five data-driven UI tests (one per row of data/logins.csv) using the Page Object.

Public site (baseline):  pytest labs/lab-5/test_ui.py -v
Local mirror (drift):    $env:APP_URL="http://127.0.0.1:5000"; pytest labs/lab-5/test_ui.py -v
Through Healenium:       $env:HEALENIUM_URL="http://localhost:8085"   (add APP_URL=http://host.docker.internal:5000 for the mirror)
"""
import csv, os, pathlib, pytest
from selenium import webdriver
from labs_lab5_pages import LoginPage  # path shim in conftest.py

DATA = pathlib.Path(__file__).parent / "data" / "logins.csv"
ROWS = list(csv.DictReader(open(DATA, encoding="utf-8")))
BASE = os.environ.get("APP_URL", "https://the-internet.herokuapp.com")


@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    hub = os.environ.get("HEALENIUM_URL")
    drv = webdriver.Remote(command_executor=hub, options=opts) if hub else webdriver.Chrome(options=opts)
    drv.set_page_load_timeout(60)
    yield drv
    drv.quit()


@pytest.mark.parametrize("row", ROWS, ids=[f"{r['username'] or 'empty'}-{r['password'][:6] or 'empty'}" for r in ROWS])
def test_login_message(driver, row):
    page = LoginPage(driver, BASE).open()
    page.login(row["username"], row["password"])
    assert row["expected_message"] in page.flash_text()
