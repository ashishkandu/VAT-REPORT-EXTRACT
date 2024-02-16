import re
from unittest.mock import patch
import httpretty

from src.customsession import CustomSession


class TestCustomSessionRetry:
    """Tests for Custom Session retry logic."""

    def setup_method(self, method):
        self.session = CustomSession("https://www.example.com")

    @httpretty.activate
    def test_session_retry_get(self):
        """Test if CBMS retry logic works as expected."""

        # Mocking a failed request with 5xx status codes for the first 2 attempts, and then a successful response
        httpretty.register_uri(
            httpretty.GET,
            re.compile(r'https://.*'),
            responses=[
                httpretty.Response(
                    body='{"message": "Internal Server Error"}',
                    status=504,
                ),
                httpretty.Response(
                    body='{"message": "Internal Server Error"}',
                    status=503,
                ),
                httpretty.Response(
                    body='{"message": "Hello World!"}',
                    status=200,
                ),
            ]
        )

        # Use the CBMS session to make a request
        with patch("time.sleep"):
            response = self.session.get(
                self.session.base_url('/status'))

        # Verify that the request was retried 3 times and then succeeded
        assert response.status_code == 200
        # Total requests (3 retries + 1 successful request)
        assert len(httpretty.latest_requests()) == 3

    @httpretty.activate
    def test_session_retry_post(self):
        """Test if CBMS retry logic works as expected."""

        # Mocking a failed request with 5xx status codes for the first 2 attempts, and then a successful response
        httpretty.register_uri(
            httpretty.POST,
            re.compile(r'https://.*'),
            responses=[
                httpretty.Response(
                    body='{"message": "Internal Server Error"}',
                    status=500,
                ),
                httpretty.Response(
                    body='{"message": "Hello World!"}',
                    status=200,
                ),
            ]
        )

        # Use the CBMS session to make a request
        response = self.session.post(
            self.session.base_url('/api/auth/login'))

        # Verify that the request was retried 3 times and then succeeded
        assert response.status_code == 200
        # Total requests (3 retries + 1 successful request)
        assert len(httpretty.latest_requests()) == 2
