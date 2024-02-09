import logging
import logging.config
import yaml
from pathlib import Path

from settings import DEFAULT_LOG_PATH


DEFAULT_LOG_LEVEL = logging.DEBUG


class LoggerFactory(object):
    """
    Reusable logger.
    """

    _LOG = None

    @staticmethod
    def __createlogger(name: str, cfg_path: Path):
        """
        A private method that interacts with the python logging module.
        """
        if cfg_path.exists():
            with open(cfg_path, 'rt') as cfg_file:
                try:
                    config = yaml.safe_load(cfg_file.read())
                    logging.config.dictConfig(config)
                except yaml.YAMLError as exc:
                    logging.basicConfig(level=DEFAULT_LOG_LEVEL)
                    logging.warning("YAMLError happened: %s", exc)

        else:
            raise FileNotFoundError("Logging configuration not found")

        LoggerFactory._LOG = logging.getLogger(name)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(
        name: str,
        cfg_path=DEFAULT_LOG_PATH,
    ):
        """
        A static method called by other modules to
        initialize logger in their own modules.

        Args:
            name (str): Name of the logger.
            cfg_path (Path, Optional): :obj:`Path` of the yaml
            config file for logging
        """
        logger = LoggerFactory.__createlogger(name, cfg_path)

        # return the logger
        return logger
