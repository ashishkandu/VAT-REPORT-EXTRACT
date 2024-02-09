from sqlalchemy import URL, create_engine
import tomli
import os
from dotenv import load_dotenv
from settings import PACKAGE_DIR

from src.loggerfactory import LoggerFactory


logger = LoggerFactory.get_logger(__name__)

db_config = PACKAGE_DIR.joinpath('src', 'config', 'db_config.toml')


if not db_config.exists():
    logger.error(f'Config file {db_config} does not exist')
    raise FileNotFoundError("Database config file not found.")


def get_sql_engine():
    with open(db_config, 'rb') as config_file:
        config_data: dict = tomli.load(config_file)

    DRIVER_NAME = config_data['driver']['name']
    SERVER_NAME = config_data['server']['name']
    DATABASE_NAME = config_data['database']['name']
    USERNAME = config_data['user']['name']
    load_dotenv()  # Load the environment containing db password
    password = os.getenv('DBpassword')
    if not password:
        logger.error('Password not found in the env!')
        raise SystemExit()
    logger.debug('DB configurations loaded successfully')

    connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={password}"
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    return create_engine(connection_url)
