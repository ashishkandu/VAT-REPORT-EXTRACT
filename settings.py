from pathlib import Path


# Base directory
PACKAGE_DIR = Path(__file__).parent.absolute()

# Logging config path
DEFAULT_LOG_PATH = PACKAGE_DIR.joinpath('src', 'config', 'logger_config.yml')

# md5 hash value
HASH_VALUE = {
    "purchase": "6d9ca675290786724f2c626f50309037",
    "sales": "771f7a36bc5518303751f41afb361f48",
    "File 1L+": "d73ff4586f22c333a5ea17e0e4c3de95",
}

# Download endpoint for template files
DOWNLOAD_REPORT_ENDPOINT = '/api/billingregister/BillingRegister/excelFile'

# Download endpoint book id
DOWNLOAD_REPORT_ID = {
    "purchase": 2,
    "sales": 1,
}

# Save downloaded file locally
DOWNLOAD = False

# Sheets directories
TEMPLATE_SAVE_DIR = PACKAGE_DIR / 'templates'
SHEETS_DIR = PACKAGE_DIR / 'sheets'
