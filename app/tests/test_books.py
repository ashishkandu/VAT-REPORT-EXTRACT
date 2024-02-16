import pytest
from src.books import ID, BookColumns, EmptyColumns, Book, Books

# Test cases for ID enum


def test_id_enum_values():
    assert ID.PURCHASE.value == 1
    assert ID.SALES.value == 2

# Test cases for BookColumns dataclass


def test_book_columns_creation():
    columns = BookColumns(['col1', 'col2'])
    assert columns.column_names == ['col1', 'col2']

# Test cases for EmptyColumns dataclass


def test_empty_columns_creation():
    emptycols = EmptyColumns([1, 3])
    assert emptycols.indices == [1, 3]

# Test cases for Book dataclass


def test_book_creation():
    book = Book(ID.PURCHASE, 'purchase', 'Nepali PB',
                BookColumns([]), 'endpoint', EmptyColumns([]))
    assert book.id == ID.PURCHASE
    assert book.name == 'purchase'
    assert book.sheet == 'Nepali PB'
    assert book.symbol == 'P'
    assert book.columns.column_names == []
    assert book.endpoint == 'endpoint'
    assert book.emptycols.indices == []

# Test cases for Books enum


def test_books_enum_values():
    assert Books.PURCHASE.value.id == ID.PURCHASE.value
    assert Books.PURCHASE.value.name == 'purchase'
    assert Books.PURCHASE.value.sheet == 'Nepali PB'
    assert Books.PURCHASE.value.endpoint == '/api/billingregister/BillingRegister/excelFile/2'
    assert Books.SALES.value.id == ID.SALES.value
    assert Books.SALES.value.name == 'sales'
    assert Books.SALES.value.sheet == 'Nepali SB'
    assert Books.SALES.value.endpoint == '/api/billingregister/BillingRegister/excelFile/1'


@pytest.mark.parametrize("book_type, expected_id, expected_name", [
    (Books.PURCHASE, 1, 'purchase'),
    (Books.SALES, 2, 'sales'),
    (Books.ONE_LAKH_PLUS, 0, 'File 1L+'),
])
def test_books(book_type, expected_id, expected_name):
    assert book_type.value.id == expected_id
    assert book_type.value.name == expected_name


def test_purchase_columns():
    purchase_columns = Books.PURCHASE.value.columns
    assert len(purchase_columns.column_names) == 7


def test_sales_columns():
    sales_columns = Books.SALES.value.columns
    assert len(sales_columns.column_names) == 7


def test_empty_columns():
    empty_columns = Books.PURCHASE.value.emptycols
    # Update this with the correct number of expected indices
    assert len(empty_columns.indices) == 2
