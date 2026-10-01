"""Page Object for the task manager page. ALL locators live here (single place to break/heal)."""
from selenium.webdriver.common.by import By


class TaskPage:
    URL = "http://127.0.0.1:5000/"
    TITLE_INPUT = (By.ID, "title-input")
    PRIORITY_INPUT = (By.ID, "priority-input")
    ADD_BUTTON = (By.ID, "add-btn")
    PENDING_COUNT = (By.ID, "pending-count")
    TASK_TITLES = (By.CSS_SELECTOR, "#task-list .task-title")
    DONE_LINKS = (By.CSS_SELECTOR, "#task-list .done-link")

    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.url = base_url or self.URL

    def open(self):
        self.driver.get(self.url)
        return self

    def add_task(self, title, priority):
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)
        p = self.driver.find_element(*self.PRIORITY_INPUT)
        p.clear(); p.send_keys(str(priority))
        self.driver.find_element(*self.ADD_BUTTON).click()
        return self

    def titles(self):
        return [e.text for e in self.driver.find_elements(*self.TASK_TITLES)]

    def pending_text(self):
        return self.driver.find_element(*self.PENDING_COUNT).text

    def complete_first(self):
        self.driver.find_elements(*self.DONE_LINKS)[0].click()
        return self
