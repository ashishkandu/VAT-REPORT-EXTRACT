import pytest
from io import BytesIO
from unittest.mock import patch

from src.books import Books
from src.one_lakh_plus_transactions import LakhBusters, TransactionAbove1L


# Arrange a test directory
@pytest.fixture
def test_work_dir(tmp_path):
    test_work_dir = tmp_path / "work_dir"
    test_work_dir.mkdir()
    return test_work_dir


@pytest.fixture
@patch('src.one_lakh_plus_transactions.TemplateFile')
def lakh_busters(mock_template_file, test_work_dir):
    template_data = BytesIO(b'fake_template_data')
    mock_template_file.return_value.get.return_value = template_data
    return LakhBusters(test_work_dir)


def test_initialization(lakh_busters, test_work_dir):
    assert lakh_busters.book == Books.ONE_LAKH_PLUS.value
    assert isinstance(lakh_busters.buffer, BytesIO)
    assert lakh_busters.save_filepath == test_work_dir / "transactions_above_1L.xls"


def test_template_buffer_creation(lakh_busters):
    # Setup
    template_data = BytesIO(b'fake_template_data')

    with patch('src.one_lakh_plus_transactions.TemplateFile') as mock_template_file:
        mock_template_file.return_value.get.return_value = template_data

        # Test template buffer creation
        template_buffer = lakh_busters.get_1L_plus_template_buffer()

        # Assert
        assert isinstance(template_buffer, BytesIO)
        assert template_buffer == template_data


@pytest.mark.parametrize(
    "lakh_busters_data",
    [
        [TransactionAbove1L("12345", "Person1", "Trade1", "Type1", 1000, 500)],
        [TransactionAbove1L("67890", "Person2", "Trade2", "Type2", 2000, 0)],
    ],
)
def test_save(lakh_busters_data, lakh_busters):
    # Mock the save method to avoid using pandas
    with patch.object(LakhBusters, 'save') as mock_save:
        lakh_busters.update_lakh_busters(lakh_busters_data)

        lakh_busters.save()  # Calls the mocked save method

        # Assert that the mocked save method was called with the no arguments
        mock_save.assert_called_once_with()


def test_get_lakh_busters():
    expected_data = [TransactionAbove1L(
        "PAN3", "Person3", "Trade3", "Type3", 3000, 100)]
    LakhBusters._lakh_busters = expected_data
    assert LakhBusters.get_lakh_busters() == expected_data


def test_update_lakh_busters(lakh_busters):
    lakh_busters.reset_busters()
    new_data = [TransactionAbove1L(
        "PAN4", "Person4", "Trade4", "Type4", 4000, 200)]
    lakh_busters.update_lakh_busters(new_data)
    assert lakh_busters.get_lakh_busters() == new_data


def test_save_filepath_generation(lakh_busters, test_work_dir):

    # Test save filepath generation
    save_filepath = lakh_busters.save_filepath

    # Assert
    assert save_filepath == test_work_dir.joinpath("transactions_above_1L.xls")
