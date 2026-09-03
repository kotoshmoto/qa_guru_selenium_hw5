import pytest
from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory


class TableElement:
    def __init__(self, root_element):
        self.root_element = root_element

    def get_headers(self) -> list[str]:
        headers = self.root_element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in headers]

    def get_row_data(self, row_index: int) -> list[str]:
        rows = self.root_element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")

        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        return self.get_row_data(row_index)[column_index]


class TablesPage(PageFactory):
    URL = "https://the-internet.herokuapp.com/tables"

    locators = {
        "table1_element": ("ID", "table1"),
        "table2_element": ("ID", "table2"),
    }

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def open(self):
        self.driver.get(self.URL)
        return self

    @property
    def table1(self) -> TableElement:
        return TableElement(self.table1_element)

    @property
    def table2(self) -> TableElement:
        return TableElement(self.table2_element)


@pytest.mark.parametrize(
    "table_name", [pytest.param("table1", id="table-1"), pytest.param("table2", id="table-2")])
def test_table_contains_data(driver, table_name):
    page = TablesPage(driver).open()

    table = getattr(page, table_name)

    headers = table.get_headers()
    first_row = table.get_row_data(0)
    due_value = table.get_cell_value(row_index=2, column_index=3)

    assert "Last Name" in headers
    assert "Smith" in first_row
    assert due_value == "$100.00"


def test_both_tables_contain_expected_data(driver):
    page = TablesPage(driver).open()

    tables = {"table1": page.table1, "table2": page.table2}

    for table_name, table in tables.items():
        headers = table.get_headers()
        first_row = table.get_row_data(0)
        due_value = table.get_cell_value(
            row_index=2,
            column_index=3,
        )

        assert "Last Name" in headers, f"{table_name}: заголовок 'Last Name' не найден"
        assert "Smith" in first_row, f"{table_name}: фамилия 'Smith' не найдена в первой строке"
        assert due_value == "$100.00", f"{table_name}: expected='$100.00', actual={due_value!r}"
