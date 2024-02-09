import yaml
from pathlib import Path
from settings import PACKAGE_DIR

from src.loggerfactory import LoggerFactory


RUNTIME_CONFIG_PATH = PACKAGE_DIR.joinpath(
    'src', 'config', 'runtime_config.yml')
# RUNTIME_CONFIG_PATH = package_dir.joinpath('runtime_config.yml')
logger = LoggerFactory.get_logger(__name__)


def get_data(key: str, config_path: Path = RUNTIME_CONFIG_PATH) -> dict:
    if config_path.exists():
        with open(config_path, 'rt') as config_file:
            try:
                config_data: dict = yaml.safe_load(config_file.read())
            except yaml.YAMLError as err:
                logger.error(
                    f"Error loading {config_path.name} cofigurations: {err}")
                raise SystemExit
            try:
                return config_data[key]
            except KeyError:
                logger.error(
                    f"{key} not found in {config_path.name} configurations")
                raise SystemExit
    else:
        error_msg = f"File {config_path} not found"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
