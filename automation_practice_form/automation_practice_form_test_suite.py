import os

import pytest

from automation_practice_form_po import AutomationPracticeFormPO


@pytest.fixture
def practice_form_page():
    url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    page = AutomationPracticeFormPO(url)
    page.setup()
    file_path = os.path.abspath("test_file.jpg")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Test")

    yield page, file_path

    if os.path.exists(file_path):
        os.remove(file_path)

    page.tear_down()


class TestAutomationPracticeForm:

    def test_form_positive01(self, practice_form_page):
        page, tmp_file_name = practice_form_page

        birth_day = ("22", "May", "1988")
        subjects = ("Maths", "English")
        hobbies = ("Sports", "Music")

        result_page = page.fill_in_form(file_name=tmp_file_name, first_name="Dmitry", last_name="Bugaev",
                                        email="bugaev@example.com", gender="Male", user_number="1234567890",
                                        birth_day=birth_day, subjects=subjects, hobbies=hobbies,
                                        current_address="г. Санкт-Петербург, ул. Невский проспект, д 101",
                                        state="NCR", city="Noida")

        result_page.assert_is_opened()
        result_page.assert_student_name("Dmitry", "Bugaev")
        result_page.assert_email("bugaev@example.com")
        result_page.assert_gender("Male")
        result_page.assert_mobile("1234567890")
        result_page.assert_birth_day(birth_day)
        result_page.assert_subjects(subjects)
        result_page.assert_hobbies(hobbies)
        result_page.assert_picture(tmp_file_name)
        result_page.assert_address("г. Санкт-Петербург, ул. Невский проспект, д 101")
        result_page.assert_state_and_city("NCR", "Noida")

    def test_form_positive02(self, practice_form_page):
        page, tmp_file_name = practice_form_page

        birth_day = ("15", "July", "2000")
        subjects = ("Physics", "Computer Science")
        hobbies = ("Reading",)

        result_page = page.fill_in_form(file_name=tmp_file_name, first_name="Ivan", last_name="Ivanov",
                                        email="ivanov@example.com", gender="Male", user_number="9876543210",
                                        birth_day=birth_day, subjects=subjects, hobbies=hobbies,
                                        current_address="Novosibirsk", state="NCR", city="Delhi")

        result_page.assert_is_opened()
        result_page.assert_student_name("Ivan", "Ivanov")
        result_page.assert_email("ivanov@example.com")
        result_page.assert_gender("Male")
        result_page.assert_mobile("9876543210")
        result_page.assert_birth_day(birth_day)
        result_page.assert_subjects(subjects)
        result_page.assert_hobbies(hobbies)
        result_page.assert_picture(tmp_file_name)
        result_page.assert_address("Novosibirsk")
        result_page.assert_state_and_city("NCR", "Delhi")
