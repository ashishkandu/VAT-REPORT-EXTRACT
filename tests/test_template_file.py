import hashlib
from urllib.parse import urljoin
import pytest
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError
from settings import HASH_VALUE

from src.books import Book
from src.cbms import CBMS, TokenAuth
from src.exceptions import BookNameNotFoundError, FileValidationError
from src.template_file import TemplateFile


@pytest.fixture
def book_mock():
    book = Mock(
        spec=Book,
        endpoint='/api/billingregister/BillingRegister/excelFile'
    )
    book.name = "purchase"
    return book


@pytest.fixture
def cbms_mock():
    return Mock(
        spec=CBMS,
        headers={},
        base_url=lambda path: urljoin("https://www.example.com/", path),
    )


@pytest.fixture
def token_auth_mock():
    return Mock(spec=TokenAuth)


@pytest.fixture
def template_file(cbms_mock, token_auth_mock):
    return TemplateFile(cbms_mock, token_auth_mock)


@pytest.fixture
def mock_response():
    # Mock response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'some file content'
    mock_response.elapsed.total_seconds.return_value = 1.23987
    return mock_response


@patch("src.template_file.TemplateFile.get_hash_value")
def test_get_successful(patched_get_hash, template_file, book_mock, cbms_mock, token_auth_mock, mock_response):

    patched_get_hash.return_value = hashlib.md5(
        mock_response.content).hexdigest()

    cbms_mock.get.return_value = mock_response

    with patch("src.template_file.DOWNLOAD", False):
        content = template_file.get(book_mock)

    assert content.getvalue() == mock_response.content
    cbms_mock.get.assert_called_once_with(
        cbms_mock.base_url(book_mock.endpoint),
        auth=token_auth_mock
    )


def test_get_failed_download(template_file, book_mock, cbms_mock):

    mock_response = Mock(status_code=404)
    mock_response.elapsed.total_seconds.return_value = 1.23987
    mock_response.raise_for_status.side_effect = HTTPError

    cbms_mock.get.return_value = mock_response

    with pytest.raises(HTTPError):
        template_file.get(book_mock)


def test_get_validation_failure(template_file, book_mock, cbms_mock, mock_response):

    cbms_mock.get.return_value = mock_response

    with patch('src.template_file.HASH_VALUE', {'purchase': 'invalid_hash'}):
        with pytest.raises(FileValidationError) as e:
            template_file.get(book_mock)

    assert 'Error validating the file against its MD5 hash' in str(e)


def test_get_hash_value_valid(template_file):
    assert template_file.get_hash_value('purchase') == HASH_VALUE['purchase']
    assert template_file.get_hash_value('sales') == HASH_VALUE['sales']


def test_get_hash_value_invalid(template_file):
    with pytest.raises(BookNameNotFoundError) as e:
        template_file.get_hash_value('invalid_book')

    assert 'Please check HASH_VALUE in configurations settings' in str(e)
