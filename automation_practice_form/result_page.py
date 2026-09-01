from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ResultPO:
    RESULT_FORM = (By.ID, "resultModal")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def _get_result_text(self) -> str:
        result_form = self.wait.until(EC.visibility_of_element_located(self.RESULT_FORM))
        return result_form.text

    def assert_is_opened(self):
        result_form = self.wait.until(EC.visibility_of_element_located(self.RESULT_FORM))

        assert result_form.is_displayed()

    def assert_student_name(self, first_name: str, last_name: str):
        expected = f"{first_name} {last_name}"
        assert expected in self._get_result_text()

    def assert_email(self, email: str):
        assert email in self._get_result_text()

    def assert_gender(self, gender: str):
        assert gender in self._get_result_text()

    def assert_mobile(self, user_number: str):
        assert user_number in self._get_result_text()

    def assert_birth_day(self, birth_day: tuple[str, str, str]):
        day, month, year = birth_day
        expected = f"{day} {month[:3]} {year}"

        assert expected in self._get_result_text()

    def assert_subjects(self, subjects: tuple[str, ...]):
        result_text = self._get_result_text()

        for subject in subjects:
            assert subject in result_text

    def assert_hobbies(self, hobbies: tuple[str, ...]):
        result_text = self._get_result_text()

        for hobby in hobbies:
            assert hobby in result_text

    def assert_picture(self, file_path: str):
        file_name = Path(file_path).name

        assert file_name in self._get_result_text()

    def assert_address(self, address: str):
        assert address in self._get_result_text()

    def assert_state_and_city(self, state: str, city: str) :
        expected = f"{state} {city}"

        assert expected in self._get_result_text()
