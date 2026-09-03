import os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory import PageFactory

from automation_practice_form.result_page import ResultPO
from calendar_with_selenium.calendar import Calendar


def create_tmp_file():
    file_path = os.path.abspath("test_file.jpg")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Test")

    return file_path


class AutomationPracticeForm(PageFactory):
    CALENDAR_INPUT = (By.ID, 'dateOfBirthInput')

    locators = {
        'practice_form_title': ('By.XPATH', '//main//h1'),
        'first_name_field': ('By.ID', 'firstName'),
        'last_name_field': ('By.ID', 'lastName'),
        'email_field': ('By.ID', 'userEmail'),
        'user_number_field': ('By.ID', 'userNumber'),
        'calendar_input': ('By.ID', 'dateOfBirthInput'),
        'year_of_birth_select': ('By.CSS_SELECTOR', '.react-datepicker__year-select'),
        'month_of_birth_select': ('By.CSS_SELECTOR', '.react-datepicker__month-select'),
        'subject_field': ('By.ID', 'subjectsInput'),
        'upload_picture_button': ('By.ID', 'uploadPicture'),
        'current_address_field': ('By.ID', 'currentAddress'),
        'state_input': ('By.ID', 'state'),
        'city_input': ('By.ID', 'city'),
        'submit_button': ('By.ID', 'submit'),
        'banner_button': ('By.Xpath', "//div[@id='fixedban']//button[@aria-label='Close']"),
        'result_form': ('By.ID', 'resultModal')
    }

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.timeout = 5
        self.wait = WebDriverWait(driver, 5)
        self.calendar = Calendar(driver=self.driver, locator=self.CALENDAR_INPUT)

    def _close_commercial_banner(self):
        self.banner_button.click_button()

    def _fill_first_name(self, first_name):
        self.first_name_field.set_text(first_name)

    def _fill_last_name(self, last_name):
        self.last_name_field.set_text(last_name)

    def _fill_email(self, email):
        self.email_field.set_text(email)

    def _fill_user_number(self, user_number):
        self.user_number_field.set_text(user_number)

    def _select_gender(self, gender):
        gender_radio_button = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='genterWrapper']//input[@value='{gender}']")
        gender_radio_button.click()

    def _upload_file(self, file_path):
        self.upload_picture_button.send_keys(file_path)

    def _fill_subject(self, subjects):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.subject_field)

        for subject in subjects:
            self.subject_field.send_keys(subject)
            self.subject_field.send_keys(Keys.ENTER)

    def _select_hobbies(self, hobbies):
        for hobby in hobbies:
            hobby_check_box = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='hobbiesWrapper']//input[@value='{hobby}']")
            hobby_check_box.click()

    def _fill_current_address(self, current_address):
        self.current_address_field.set_text(current_address)

    def _select_state(self, state):
        self.state_input.click_button()
        state_dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@class='state-city-option'][text()='{state}']")))
        state_dropdown.click()

    def _select_city(self, city):
        self.city_input.click_button()
        city_dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[@class='state-city-option'][text()='{city}']")))
        city_dropdown.click()

    def _click_submit_button(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.submit_button)
        self.submit_button.click_button()

        return ResultPO(self.driver)

    def fill_in_form(self, file_name=None, first_name=None, last_name=None, email=None, gender=None, user_number=None,
                     birth_day=None, subjects=None, hobbies=None, current_address=None, state=None,
                     city=None) -> ResultPO:

        assert self.practice_form_title.get_text() == "Practice Form", "Заголовок страницы не совпадает"

        if file_name is None:
            file_name = self._create_tmp_file()

        self._close_commercial_banner()

        self._fill_first_name(first_name)
        self._fill_last_name(last_name)
        self._fill_email(email)

        self._select_gender(gender)

        self._fill_user_number(user_number)

        self.calendar.select_date(birth_day)

        self._fill_subject(subjects)
        self._select_hobbies(hobbies)

        self._upload_file(file_name)

        self._fill_current_address(current_address)

        self._select_state(state)
        self._select_city(city)

        return self._click_submit_button()
