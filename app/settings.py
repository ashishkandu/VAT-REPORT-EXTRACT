from pathlib import Path

# Define the base directory using the absolute path of the current file
PACKAGE_PATH = Path(__file__).parent.absolute()
PACKAGE_DIR = PACKAGE_PATH.parent

# Google API credentials
GOOGLE_API_CREDENTIALS = PACKAGE_DIR.joinpath('client_secrets.json')
TOKEN_PATH = PACKAGE_PATH / 'token.json'

# Set the path to your client secrets JSON file
DRIVE_CACHE_PATH = PACKAGE_PATH / 'drive_cache.json'

# Define the default logging configuration file path
DEFAULT_LOG_PATH = PACKAGE_PATH.joinpath('src', 'config', 'logger_config.yml')

# Define the path to the runtime configuration file
RUNTIME_CONFIG_PATH = PACKAGE_PATH.joinpath(
    'src', 'config', 'runtime_config.yml')

# Define the location of the database config file
DB_CONFIGURATION_PATH = PACKAGE_PATH.joinpath(
    'src', 'config', 'db_config.toml')

# Define the md5 hash values for different categories
HASH_VALUE = {
    "purchase": "049d24b495a61c448933088c553cbe95",
    "sales": "52ec175d67122cf0d5ed3d60eeb8e77a",
    "File 1L+": "d73ff4586f22c333a5ea17e0e4c3de95",
}

# Define the download endpoint for template files
DOWNLOAD_REPORT_ENDPOINT = '/api/billingregister/BillingRegister/excelFile'

# Define the download endpoint book id for different categories
DOWNLOAD_REPORT_ID = {
    "purchase": 2,
    "sales": 1,
}

# Set the flag to determine whether to save the downloaded file locally
DOWNLOAD = False

# Define the directories for template files and sheets
TEMPLATE_SAVE_DIR = PACKAGE_PATH / 'templates'
SHEETS_DIR = PACKAGE_PATH / 'sheets'
