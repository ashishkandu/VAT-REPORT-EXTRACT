import yaml
from pathlib import Path
from settings import RUNTIME_CONFIG_PATH

from src.loggerfactory import LoggerFactory


# Get the logger instance
logger = LoggerFactory.get_logger(__name__)


def get_data(key: str, config_path: Path = RUNTIME_CONFIG_PATH) -> dict:
    """
    Get the data for a specific key from the configuration file.

    Args:
    key (str): The key to retrieve the data for.
    config_path (Path): The path to the configuration file. Defaults to RUNTIME_CONFIG_PATH.

    Returns:
    dict: The data for the specified key.

    Raises:
    FileNotFoundError: If the configuration file is not found.
    """
    if config_path.exists():
        with open(config_path, 'rt') as config_file:
            try:
                config_data: dict = yaml.safe_load(config_file.read())
            except yaml.YAMLError as err:
                # Log error if there's an issue loading the configuration
                logger.error(
                    f"Error loading {config_path.name} configurations: {err}")
                raise SystemExit
            try:
                return config_data[key]
            except KeyError:
                # Log error if the key is not found in the configuration
                logger.error(
                    f"{key} not found in {config_path.name} configurations")
                raise SystemExit
    else:
        # Log error if the configuration file is not found
        error_msg = f"File {config_path} not found"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
