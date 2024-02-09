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

    """
    # Log the action
    logger.info(f'Saving contents to {filepath.name}')

    # Write the data to the file
    parent_path = filepath.parent
    parent_path.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(buffer.getvalue())

    # Log the completion
    logger.info('File write completed!')
