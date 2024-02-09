import pytest
from unittest.mock import Mock
from src.one_lakh_plus_transactions import LakhBusters
from src.report_generator import ReportGenerator, Book, FilingMonth, Report


@pytest.fixture
def filing_month():
    return FilingMonth(2080, 2)


def test_generate_with_single_book(filing_month, monkeypatch):
    # Arrange
    report_generator = ReportGenerator(filing_month)
    mock_book = Mock(spec=Book)
    mock_report = Mock(spec=Report)
    monkeypatch.setattr(report_generator, 'get_report',
                        lambda book: mock_report)

    # Act
    report_generator.generate(mock_book)

    # Assert
    mock_report.save.assert_called_once()
    mock_report.print_cancelled_transactions.assert_called_once()
    mock_report.print_transactions_with_roundoff.assert_called_once()


def test_generate_with_multiple_books(filing_month, monkeypatch):
    # Arrange
    report_generator = ReportGenerator(filing_month)
    mock_purchase_report = Mock(spec=Report)
    mock_sales_report = Mock(spec=Report)

    mock_lakh_busters = Mock(spec=LakhBusters)

    monkeypatch.setattr(ReportGenerator, 'lakh_busters', mock_lakh_busters)
    monkeypatch.setattr(report_generator, 'get_report',
                        lambda book: mock_purchase_report if book.id == 1 else mock_sales_report)

    # Act
    report_generator.generate(None)

    # Assert
    mock_purchase_report.save.assert_called_once()
    mock_purchase_report.print_cancelled_transactions.assert_called_once()
    mock_purchase_report.print_transactions_with_roundoff.assert_called_once()
    mock_sales_report.save.assert_called_once()
    mock_sales_report.print_cancelled_transactions.assert_called_once()
    mock_sales_report.print_transactions_with_roundoff.assert_called_once()


def test_get_report(filing_month):
    # Arrange
    report_generator = ReportGenerator(filing_month)
    mock_book = Mock(spec=Book)
    mock_book.name = "book1"
    expected_report = Report(mock_book, filing_month,
                             report_generator.work_dir)
    report_generator.get_report = lambda book: expected_report

    # Act
    report = report_generator.get_report(mock_book)

    # Assert
    assert report == expected_report
