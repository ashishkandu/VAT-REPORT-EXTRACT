from io import BytesIO
from pathlib import Path

from src.loggerfactory import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


def write_bytes_to_disk(buffer: BytesIO, filepath: Path):
    """It writes bytes formatted data to provided filepath."""
    logger.info(f'Saving contents to {filepath.name}')
    with open(filepath, 'wb') as filepath:
        filepath.write(buffer.getvalue())
    logger.info('File write completed!')
