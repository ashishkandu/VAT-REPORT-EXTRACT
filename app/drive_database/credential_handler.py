import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

from settings import GOOGLE_API_CREDENTIALS, TOKEN_PATH
from src.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)

# Define the scope for Google Drive API
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/docs',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]


logger = logging.getLogger(__name__)


def save_token(credentials: Credentials):
    """
    Saves the obtained credentials to the token file.
    """
    try:
        with TOKEN_PATH.open('w') as token_file:
            token_file.write(credentials.to_json())
            token_file.flush()
            logger.debug('Confirmed successful write operation')
    except Exception as e:
        logger.error(f'Failed to save token: {e}')


def request_credentials():
    """
    Requests and returns Google API credentials for accessing Google services.
    If the credentials file and token file exist, it tries to retrieve the cached credentials,
    otherwise it runs the local server for authentication and saves the obtained credentials to the token file.
    """

    # Check if Google API credentials file exists
    if not GOOGLE_API_CREDENTIALS.exists():
        raise FileNotFoundError(
            f'Client secrets file not found: {GOOGLE_API_CREDENTIALS}')

    # Check if token file exists
    if TOKEN_PATH.exists():
        return get_cached_credentials()

    # Create the OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_API_CREDENTIALS, SCOPES)

    logger.debug('Running local server for authentication')
    credentials = flow.run_local_server(port=0)

    save_token(credentials=credentials)

    return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)


def get_cached_credentials():
    """Get credentials from cached token file."""

    logger.debug('Retrieving credentials from cached token file')
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # Check if credentials are expired and can be refreshed
    if creds and creds.expired and creds.refresh_token:
        logger.info('Token expired, refreshing...')
        try:
            creds.refresh(Request())
            save_token(credentials=creds)
        except RefreshError as e:
            logger.error(f'Error refreshing credentials: {e}')
    return creds
