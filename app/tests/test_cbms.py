from unittest.mock import Mock, patch
import pytest
import requests

from src.cbms import CBMS, TokenAuth


@pytest.fixture
def mock_response():
    # Mock response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.elapsed.total_seconds.return_value = 1.23987
    mock_response.json.return_value = {
        'isSucess': True,
        'token': 'mock_token',
        'responseData': {
            'userName': 'Mock User',

        }
    }
    return mock_response


@pytest.fixture
def mock_response_failure():
    mock_response = Mock()
    # Simulate API returning 200 even on failure
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "isSucess": False,
        "message": "Invalid Username or Password !!!"
    }
    mock_response.elapsed.total_seconds.return_value = 2.122

    return mock_response


class TestCBMS:

    def setup_method(self, method):
        TokenAuth.reset_token()  # Clear the token for all instances before each test

    def teardown_method(self, method):
        patch.stopall()  # Ensure any mocks are cleaned up

    @patch('requests.Session.post')
    def test_login_success(self, mock_post, mock_response: Mock):
        mock_post.return_value = mock_response

        auth = TokenAuth()
        assert auth._TOKEN == 'Bearer mock_token'  # Verify token is set correctly

    @patch('requests.Session.post')
    def test_login_failure(self, mock_post, mock_response_failure: Mock):
        mock_post.return_value = mock_response_failure  # Inject the mock response

        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            TokenAuth()  # Should raise HTTPError due to failed login
        assert 'Invalid Username or Password !!!' in str(excinfo.value)

    def test_cbms_session_creation(self):
        client = CBMS()
        assert isinstance(client, requests.Session)
        # Check default headers (adjusted assertion)
        assert client.headers['User-Agent'].startswith('Mozilla/5.0')

    def test_cbms_base_url(self):
        client = CBMS()
        assert client.base_url(
            '/some/endpoint') == 'https://cbms.ird.gov.np:8051/some/endpoint'
