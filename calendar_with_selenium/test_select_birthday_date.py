from automation_practice_form_page_selenium import AutomationPracticeFormPage


def test_select_birthday_date(driver):
    page = AutomationPracticeFormPage(driver)
    page.birthday_calendar.select_date(("15", "July", "2000"))

    assert (page.birthday_calendar.get_value() == "15 Jul 2000")
