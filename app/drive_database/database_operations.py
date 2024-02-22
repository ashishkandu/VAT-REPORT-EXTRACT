import os
from pathlib import Path

import pyodbc
import tomli
from src.loggerfactory import LoggerFactory

from settings import DB_CONFIGURATION_PATH


logger = LoggerFactory.get_logger(__name__)

mssql_data = Path('/var/opt/mssql/data')
logger.debug(f'Backup will be restored in {str(mssql_data)}')

# Connection parameters
logger.debug(f'Loading configruation from {DB_CONFIGURATION_PATH}')
with open(DB_CONFIGURATION_PATH, 'rb') as config_file:
    config_data: dict = tomli.load(config_file)

DRIVER = config_data['driver']['name']
SERVER = config_data['server']['name']
DATABASE_NAME = config_data['database']['name']
UID = config_data['user']['name']
PWD = os.getenv('SA_PASSWORD')

database = 'master'
connection_string = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={database};UID={UID};PWD={PWD}"


def restore(
    filepath: Path,
    connection_string=connection_string,
    DATABASE_NAME=DATABASE_NAME,
    mssql_data=mssql_data
):
    """Restore the database from a backup file.

    Args:
        filepath (Path): The path to the backup file.
        connection_string (str): The connection string for pyodbc.
        DATABASE_NAME (str): The name of the database to be restored.
        mssql_data (Path): The path to the MS SQL data directory.
    """
    logger.info("Attempting to establish connection...")
    # Create connection
    try:
        conn = pyodbc.connect(connection_string)
    except pyodbc.Error as e:
        logger.error(f"Failed to connect to database: {e}")
        return

    logger.info("Connection established successfully!")

    conn.autocommit = True

    # Open cursor
    cursor = conn.cursor()

    logger.debug(f"Executing RESTORE FILELISTONLY for {filepath}...")

    # Retrieve file list from backup
    cursor.execute(f"""
    RESTORE FILELISTONLY FROM DISK = N'{filepath}'
    """)

    # Process file list
    files = {}
    for row in cursor.fetchall():
        # Process file list from backup
        # Each row contains the following information:
        # row[2]: symbol ['D', 'L']
        # row[0]: logical name ['VatBillingSoftware', 'VatBillingSoftware_log']
        # row[1]: physical name
        # - ['F:\\Billing Software\\Database\\VatBillingSoftware.mdf',
        #    'F:\\Billing Software\\Database\\VatBillingSoftware_log.ldf']

        files[row[2]] = {
            'logical_name': row[0],
            'physical_name': row[1].split('\\')[-1]
        }

    logger.debug(
        f"Executing RESTORE DATABASE for {DATABASE_NAME} from {filepath}...")

    # Restore database from backup
    cursor.execute(f"""
        RESTORE DATABASE {DATABASE_NAME} FROM DISK=N'{filepath}' WITH REPLACE,
        MOVE '{files['D']['logical_name']}' TO '{mssql_data.joinpath(files['D']['physical_name'])}',
        MOVE '{files['L']['logical_name']}' TO '{mssql_data.joinpath(files['L']['physical_name'])}'
        """)

    while cursor.nextset():
        logger.info("Restoring databse...")

    logger.info(
        f"Database {DATABASE_NAME} backup restored successfully from {filepath}")
