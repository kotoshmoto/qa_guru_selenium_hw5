from selene import browser, by, have

#https://github.com/yashaka/selene

class Calendar:
    def __init__(self, base_element):
        self.input_field = base_element

    def select_date(self, day: str, month: str, year: str):
        self.input_field.click()

        browser.element('//*[@id="fixedban"]/div/div/button').click()
        browser.element(".react-datepicker__month-select").click().element(by.text(month)).click()
        browser.element(".react-datepicker__year-select").click().element(by.text(year)).click()
        day_padded = day.zfill(3)
        browser.element(f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)").click()

class AutomationPracticeFormPage:
    def __init__(self):
        browser.open("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
        self.birthday_calendar = Calendar(browser.element("#dateOfBirthInput"))

class TestSuite:
    def test_select_birthday_date(self):
        page = AutomationPracticeFormPage()
        page.birthday_calendar.select_date(day="15", month="July", year="2000")
        page.birthday_calendar.input_field.should(have.value("15 Jul 2000"))

ts = TestSuite()
ts.test_select_birthday_date()

