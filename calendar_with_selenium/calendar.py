from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Calendar:
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")

    def __init__(self, driver, locator):
        self.wait = WebDriverWait(driver, 5)
        self.driver = driver
        self.locator = locator

    def select_date(self, date: Tuple[str, str, str]):
        day, month, year = date

        self.wait.until(EC.element_to_be_clickable(self.locator)).click()

        month_element = self.wait.until(EC.element_to_be_clickable(self.MONTH_OF_BIRTH_SELECT))
        Select(month_element).select_by_visible_text(month)

        year_element = self.wait.until(EC.element_to_be_clickable(self.YEAR_OF_BIRTH_SELECT))
        Select(year_element).select_by_visible_text(year)

        day_locator = (
            By.CSS_SELECTOR, f".react-datepicker__day--{day.zfill(3)}:not(.react-datepicker__day--outside-month)")

        self.wait.until(EC.element_to_be_clickable(day_locator)).click()

    def get_value(self):
        return self.wait.until(EC.visibility_of_element_located(self.locator)).get_attribute("value")
