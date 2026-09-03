import pytest
import time
from text_box_page import TextBoxPage


# 1. Создание виртуального окружения
# python -m venv venv

# 1.5 Если не отработал пункт 2 под Windows
# PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Активация (Для Windows)
# venv\Scripts\activate
# 2. Активация (Для macOS/Linux)
# source venv/bin/activate

# 3. Установка зависимостей
# pip install -r requirements.txt

# 4. Запуск всех тестов
# pytest -v test_text_box.py

# 4. Запуск конкретного параметризованного метода (TestSuite)
# pytest -v test_text_box.py::test_empty_form_submission

# 4. Запуск конкретного тест-кейса из параметризованного набора
# pytest test_text_box.py::test_positive_form_submission[John Doe-john@example.com-123 Elm St-456 Oak St] -v

# --- 1. Позитивные сценарии (Валидные данные) ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("John Doe", "john@example.com", "123 Elm St", "456 Oak St"),  # Стандартный кейс
    ("Иван Иванов", "ivan@mail.ru", "ул. Ленина, д. 1", "ул. Пушкина, д. 2"),  # Кириллица
    ("A", "a@b.cc", "B", "C"),  # Минимальная длина строк
    ("Name-With Dash", "dash@email.co.uk", "Addr 1/2", "Addr 3 & 4"),  # Спецсимволы в полях
    ("   John   ", "spaces@test.com", "  Street 1  ", "  Street 2  "),  # Строки с пробелами
])
def test_positive_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name, email, cur_addr, perm_addr)
    page.submit()

    output = page.get_output_data()

    expected = {
        "name": name.strip(),
        "email": email.strip(),
        "cur_addr": cur_addr.strip(),
        "perm_addr": perm_addr.strip(),
    }

    assert output is not None, "Блок с результатами не отобразился"
    assert output == expected


# --- 2. Частичное заполнение обязательных/необязательных полей ---
@pytest.mark.parametrize("name, email, cur_addr, perm_addr", [
    ("Only Name", "", "", ""),
    ("", "only@email.com", "", ""),
    ("", "", "Only Current Address", ""),
    ("", "", "", "Only Permanent Address"),
    ("Name & Email", "name_email@test.com", "", ""),
])
def test_partial_form_submission(driver, name, email, cur_addr, perm_addr):
    page = TextBoxPage(driver)
    page.open()
    page.fill_form(name, email, cur_addr, perm_addr)
    page.submit()
    output = page.get_output_data()

    assert output is not None, "Форма должна отправляться при частичном заполнении"
    if name: assert output["name"] == name
    if email: assert output["email"] == email
    if cur_addr: assert output["cur_addr"] == cur_addr
    if perm_addr: assert output["perm_addr"] == perm_addr


# --- 3. Негативные сценарии (Невалидный Email) ---
@pytest.mark.parametrize("invalid_email, expected_valid", [
    pytest.param("plainaddress", 'Адрес электронной почты должен содержать символ "@". '
                                 'В адресе "plainaddress" отсутствует символ "@".'),  # Нет собаки и домена
    pytest.param("@no-local-part.com", 'Введите часть адреса до символа \"@\".'
                                       ' Адрес \"@no-local-part.com\" неполный.'),  # Нет имени пользователя
    pytest.param("john.doe@com", 'Введите часть адреса после символа \"@\".'
                                 ' Адрес \"john.doe@com\" неполный.'),
    # Нет доменной зоны верхнего уровня - TODO: обратите особое внимание
    pytest.param("john@missing-dot", "Адрес john@missing-dot имеет некорректный формат. Адрес должен содержать"
                                     "точку в домене"),  # Нет точки в домене - TODO: обратите особое внимание
    pytest.param("john@@example.com", "Часть адреса до символа \"@\" не должна содержать символ \"\"\"."),  # Две собаки

    pytest.param("john@example..com", "Недопустимое положение символа \".\" в адресе \"example..com\".")
    # Две точки подряд
])
def test_invalid_email_validation(driver, invalid_email, expected_valid):
    page = TextBoxPage(driver)
    page.open()

    page.fill_form(name="Test", email=invalid_email)
    page.submit()

    actual_message = page.get_email_validation_message()

    assert actual_message == expected_valid


# --- 4. Граничные значения и нагрузка на длину полей (Длинные строки) ---
@pytest.mark.parametrize("field_type, form_data", [
    ("name", {"name": "A" * 1000}),
    ("email", {"email": f"{'b' * 64}@example.com"}),
    ("cur_addr", {"cur_addr": "Current " * 200}),
    ("perm_addr", {"perm_addr": "Permanent " * 200}),
]
                         )
def test_long_input_fields(driver, field_type, form_data):
    page = TextBoxPage(driver).open()

    page.fill_form(**form_data)
    page.submit()

    output = page.get_output_data()

    assert output is not None, f"Форма не справилась с длинной строкой в поле {field_type}"


# --- 5. Безопасность и спец-инъекции (XSS, SQLi, Эмодзи) ---
@pytest.mark.parametrize("payload", ["1' OR '1'='1", ":):):):))))::;)"])
def test_special_inputs(driver, payload):
    page = TextBoxPage(driver).open()

    page.fill_form(name=payload)
    page.submit()

    output = page.get_output_data()

    assert output is not None
    assert output["name"] == payload


@pytest.mark.parametrize("payload", ["<script>alert('xss')</script>", "<div>HTML injection</div>"])
def test_html_injection(driver, payload):
    page = TextBoxPage(driver).open()

    page.fill_form(name=payload)
    page.submit()

    output = page.get_output_data()

    assert output is not None


# --- 6. Пустая форма ---
def test_empty_form_submission(driver):
    page = TextBoxPage(driver).open()
    page.submit()
    output = page.get_output_data()

    time.sleep(3)  # tmp solution

    # Зависит от требований: либо форма не отправляется (None), либо пустые строки
    if output is not None:
        assert output["name"] == ""
        assert output["email"] == ""
