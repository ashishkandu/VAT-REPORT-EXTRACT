from pathlib import Path

# Define the base directory using the absolute path of the current file
PACKAGE_DIR = Path(__file__).parent.absolute()

# Define the default logging configuration file path
DEFAULT_LOG_PATH = PACKAGE_DIR.joinpath('src', 'config', 'logger_config.yml')

# Define the path to the runtime configuration file
RUNTIME_CONFIG_PATH = PACKAGE_DIR.joinpath(
    'src', 'config', 'runtime_config.yml')

# Define the location of the database config file
DB_CONFIGURATION_PATH = PACKAGE_DIR.joinpath('src', 'config', 'db_config.toml')

# Define the md5 hash values for different categories
HASH_VALUE = {
    "purchase": "6d9ca675290786724f2c626f50309037",
    "sales": "771f7a36bc5518303751f41afb361f48",
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
TEMPLATE_SAVE_DIR = PACKAGE_DIR / 'templates'
SHEETS_DIR = PACKAGE_DIR / 'sheets'
