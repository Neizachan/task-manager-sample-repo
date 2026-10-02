"""Page Object for the login page of https://the-internet.herokuapp.com/login (and its local mirror).
All locators live here, so a locator change touches one place. Explicit waits make the tests tolerant of a slow site."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 30  # seconds


class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def _wait_page_loaded(self):
        WebDriverWait(self.driver, TIMEOUT).until(
            lambda d: d.execute_script("return document.readyState") == "complete")

    def open(self):
        self.driver.get(self.base_url + "/login")
        self._wait_page_loaded()
        return self

    def login(self, username, password):
        u = self.driver.find_element(*self.USERNAME)   # plain lookup: this is where locator drift shows up / heals
        u.clear(); u.send_keys(username)
        p = self.driver.find_element(*self.PASSWORD)
        p.clear(); p.send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()
        return self

    def flash_text(self):
        # wait for the NEXT page's message instead of reading it instantly after the click
        el = WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.FLASH))
        return el.text
