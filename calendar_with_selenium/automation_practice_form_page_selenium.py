from selenium.webdriver.common.by import By

from calendar_with_selenium.calendar import Calendar


class AutomationPracticeFormPage:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.URL)

        self.birthday_calendar = Calendar(driver, self.CALENDAR_INPUT)
