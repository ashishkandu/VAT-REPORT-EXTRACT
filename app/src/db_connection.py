from sqlalchemy import URL, create_engine
import tomli
import os
from settings import DB_CONFIGURATION_PATH

from src.loggerfactory import LoggerFactory


class SQLEngine:
    _sql_engine = None

    logger = LoggerFactory.get_logger(__name__)

    @classmethod
    def _get_sql_engine(cls):
        """Get the SQL engine based on the config file"""
        
        if not DB_CONFIGURATION_PATH.exists():
            # Log an error and raise an exception if the config file does not exist
            cls.logger.error(f'Config file {DB_CONFIGURATION_PATH} does not exist')
            raise FileNotFoundError("Database config file not found.")
        
        with open(DB_CONFIGURATION_PATH, 'rb') as config_file:
            config_data: dict = tomli.load(config_file)

        DRIVER_NAME = config_data['driver']['name']
        SERVER_NAME = config_data['server']['name']
        DATABASE_NAME = config_data['database']['name']
        USERNAME = config_data['user']['name']

        password = os.getenv('SA_PASSWORD')
        if not password:
            cls.logger.error('Password not found in the env!')
            raise SystemExit()
        cls.logger.debug('DB configurations loaded successfully')

        # Construct the connection string
        connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};UID={USERNAME};PWD={password}"
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        return create_engine(connection_url)
    
    @classmethod
    def get(cls):
        if cls._sql_engine is None:
            cls._sql_engine = cls._get_sql_engine()
        return cls._sql_engine
    
    @classmethod
    def reset(cls):
        cls._sql_engine = None
