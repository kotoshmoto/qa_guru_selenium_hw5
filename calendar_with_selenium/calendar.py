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
        # Переписать например такое Selenium решение на Selene - посмотреть насколько проще итоговый код
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        ## Находим и кликаем по кнопке закрытия (крестику) модального окна
        close_banner_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
        close_banner_btn.click()
        ## Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        self.wait.until(EC.invisibility_of_element(close_banner_btn))

        self.wait.until(EC.element_to_be_clickable(self.locator)).click()

        month_element = self.wait.until(EC.element_to_be_clickable(self.MONTH_OF_BIRTH_SELECT))
        Select(month_element).select_by_visible_text(date[0])

        year_element = self.wait.until(EC.element_to_be_clickable(self.YEAR_OF_BIRTH_SELECT))
        Select(year_element).select_by_visible_text(date[1])

        day_locator = (
            By.CSS_SELECTOR, f".react-datepicker__day--{date[2].zfill(3)}:not(.react-datepicker__day--outside-month)")

        self.wait.until(EC.element_to_be_clickable(day_locator)).click()

    def get_value(self):
        return self.wait.until(EC.visibility_of_element_located(self.locator)).get_attribute("value")
