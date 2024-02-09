import os
import requests
from requests.auth import AuthBase
from dotenv import load_dotenv
from src.customsession import CustomSession

from src.loggerfactory import LoggerFactory


load_dotenv()

logger = LoggerFactory.get_logger(__name__)

BASE_URL = 'https://cbms.ird.gov.np:8051'
LOGIN_ENDPOINT = '/api/auth/login'


class CBMS(CustomSession):
    def __init__(self, base_url=BASE_URL):
        """Returns a custom session optimized to connect CBMS portal."""
        super().__init__(base_url)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Origin': 'https://cbms.ird.gov.np:8060',
            'Referer': 'https://cbms.ird.gov.np:8060/',
        }


class TokenAuth(AuthBase):
    """Implements a token authentication scheme to work with CBMS session."""

    _TOKEN = None

    def __init__(self):
        """Fetches token from the CBMS."""
        if TokenAuth._TOKEN is None:
            logger.info("Fetching new token")
            TokenAuth.__fetch_token()

    def __call__(self, request):
        """Attach an API token to a custom auth header."""
        request.headers['Authorization'] = TokenAuth._TOKEN
        return request

    @classmethod
    def reset_token(cls):
        """Resets the class-level cached token to None."""
        cls._TOKEN = None

    @staticmethod
    def __fetch_token():
        client = CBMS()
        json_data = {
            'PAN': os.getenv('PAN'),
            'LoginId': os.getenv('LoginId'),
            'password': os.getenv('password'),
            'isSuperAdmin': False,
        }

        response = client.post(
            url=client.base_url(LOGIN_ENDPOINT), json=json_data, timeout=30)
        logger.info(
            f"{response.request.method} {response.url} [status:{response.status_code} request:{response.elapsed.total_seconds():.3f}s]")
        response.raise_for_status()
        response_json = response.json()
        if not response_json.get('isSucess'):
            logger.error(f"Login failed: {response_json.get('message')}")
            raise requests.exceptions.HTTPError(response_json.get('message'))
        else:
            response_data = response.json().get('responseData')
            user_name = response_data.get('userName')  # userNameText
            logger.info(
                f"Successfully logged in to CBMS Portal as {user_name}")
            TokenAuth._TOKEN = " ".join(
                ('Bearer', response.json()['token']))
