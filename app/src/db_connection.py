from sqlalchemy import URL, create_engine
import tomli
import os
from settings import DB_CONFIGURATION_PATH

from src.loggerfactory import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


if not DB_CONFIGURATION_PATH.exists():
    # Log an error and raise an exception if the config file does not exist
    logger.error(f'Config file {DB_CONFIGURATION_PATH} does not exist')
    raise FileNotFoundError("Database config file not found.")


def get_sql_engine():
    """Get the SQL engine based on the config file"""
    with open(DB_CONFIGURATION_PATH, 'rb') as config_file:
        config_data: dict = tomli.load(config_file)

    DRIVER_NAME = config_data['driver']['name']
    SERVER_NAME = config_data['server']['name']
    DATABASE_NAME = config_data['database']['name']
    USERNAME = config_data['user']['name']

    password = os.getenv('SA_PASSWORD')
    if not password:
        logger.error('Password not found in the env!')
        raise SystemExit()
    logger.debug('DB configurations loaded successfully')

    # Construct the connection string
    connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={password}"
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    return create_engine(connection_url)
