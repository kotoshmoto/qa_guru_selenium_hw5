from automation_practice_form.automation_practice_form_po import AutomationPracticeFormPO


def test_fill_form():
    page = AutomationPracticeFormPO("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
    page.setup()

    birth_day = ("15", "July", "2000")
    subjects = ("Maths", "English")
    hobbies = ("Sports", "Music")

    result_page = page.fill_in_form(first_name="Ivan", last_name="Ivanov", email="test@test.com", gender="Male",
                                    user_number="1234567890", birth_day=birth_day, subjects=subjects, hobbies=hobbies,
                                    current_address="Novosibirsk", state="NCR", city="Delhi")

    result_page.assert_is_opened()
    result_page.assert_student_name("Ivan", "Ivanov")
    result_page.assert_email("test@test.com")
    result_page.assert_gender("Male")
    result_page.assert_mobile("1234567890")
    result_page.assert_birth_day(birth_day)
    result_page.assert_subjects(subjects)
    result_page.assert_hobbies(hobbies)
    result_page.assert_address("Novosibirsk")
    result_page.assert_state_and_city("NCR", "Delhi")

    page.tear_down()
