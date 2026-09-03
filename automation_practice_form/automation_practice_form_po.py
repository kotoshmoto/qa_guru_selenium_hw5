import os

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from calendar_with_selenium.calendar import Calendar
from result_page import ResultPO


class AutomationPracticeFormPO:
    def __init__(self, url):
        self.url = url

    PRACTICE_FORM_TITLE = (By.XPATH, "//main//h1")
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "userEmail")
    USER_NUMBER_FIELD = (By.ID, "userNumber")
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")
    SUBJECT_FIELD = (By.ID, "subjectsInput")
    UPLOAD_PICTURE_BUTTON = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    BANNER_BUTTON = (By.XPATH, "//div[@id='fixedban']//button[@aria-label='Close']")
    RESULT_FORM = (By.ID, "resultModal")

    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait = 5
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.get(self.url)

        self.calendar = Calendar(driver=self.driver, locator=self.CALENDAR_INPUT)

    def _create_tmp_file(self):
        file_path = os.path.abspath("test_file.jpg")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Test")

        return file_path

    def _close_commercial_banner(self):
        banner_button = self.wait.until(ec.element_to_be_clickable(self.BANNER_BUTTON))
        banner_button.click()

    def _fill_first_name(self, first_name):
        firstname_field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        firstname_field.send_keys(first_name)

    def _fill_last_name(self, last_name):
        lastname_field = self.driver.find_element(*self.LAST_NAME_FIELD)
        lastname_field.send_keys(last_name)

    def _fill_email(self, email):
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        email_field.send_keys(email)

    def _fill_user_number(self, user_number):
        user_number_field = self.driver.find_element(*self.USER_NUMBER_FIELD)
        user_number_field.send_keys(user_number)

    def _select_gender(self, gender):
        gender_radio_button = self.driver.find_element(By.XPATH,
                                                       f"//div[@id='genterWrapper']//input[@value='{gender}']")
        gender_radio_button.click()

    def _upload_file(self, file_path):
        self.driver.find_element(*self.UPLOAD_PICTURE_BUTTON).send_keys(file_path)

    def _fill_subject(self, *subjects):
        subjects_input = self.driver.find_element(*self.SUBJECT_FIELD)
        self.driver.execute_script("arguments[0].scrollIntoView();", subjects_input)
        for subject in subjects[0]:
            subjects_input.send_keys(subject)
            subjects_input.send_keys(Keys.ENTER)

    def _select_hobbies(self, *hobbies):
        try:
            for hobby in hobbies[0]:
                hobby_check_box = self.driver.find_element(By.XPATH,
                                                           f"//div[@id='hobbiesWrapper']//input[@value='{hobby}']")
                hobby_check_box.click()
        except NoSuchElementException as ex:
            print(ex)
        except InvalidSelectorException as ex:
            print(ex)

    def _fill_current_address(self, current_address):
        current_address_field = self.driver.find_element(*self.CURRENT_ADDRESS_FIELD)
        current_address_field.send_keys(current_address)

    def _select_state(self, state):
        self.driver.find_element(*self.STATE_INPUT).click()
        state_dropdown = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{state}']")))
        state_dropdown.click()

    def _select_city(self, city):
        self.driver.find_element(*self.CITY_INPUT).click()
        city_dropdown = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f"//div[@class='state-city-option'][text()='{city}']")))
        city_dropdown.click()

    def _click_submit_button(self):
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

        return ResultPO(self.driver)

    def fill_in_form(self, file_name=None, first_name=None, last_name=None, email=None, gender=None, user_number=None,
                     birth_day=None, subjects=None, hobbies=None, current_address=None, state=None,
                     city=None) -> ResultPO:

        practice_form_title = self.driver.find_element(*self.PRACTICE_FORM_TITLE)

        assert practice_form_title.text == "Practice Form", "Заголовок страницы не совпадает"

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

    def tear_down(self):
        self.driver.quit()
