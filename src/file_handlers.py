from io import BytesIO
from pathlib import Path

from src.loggerfactory import LoggerFactory


# Get the logger instance
logger = LoggerFactory.get_logger(__name__)


def write_bytes_to_disk(buffer: BytesIO, filepath: Path):
    """Write bytes-formatted data to the provided filepath.

    Args:
        buffer (BytesIO): The bytes-formatted data to be written.
        filepath (Path): The file path to write the data to.

    Returns:
        None

    Raises:
        FileNotFoundError: If the parent directories cannot be created.
        PermissionError: If there is an error writing to the file.

    """
    # Log the action
    logger.debug(f'Saving contents to {filepath.name}')

    # Write the data to the file
    parent_path = filepath.parent
    if not parent_path.exists():
        try:
            parent_path.mkdir(parents=True)
        except FileNotFoundError as e:
            logger.error(f'Error creating parent directories: {e}')
            raise

    try:
        with filepath.open('wb') as file:
            file.write(buffer.getvalue())
    except PermissionError as e:
        logger.error(f'Error writing to file: {e}')
        raise

    # Log the completion
    logger.info('File write completed!')
