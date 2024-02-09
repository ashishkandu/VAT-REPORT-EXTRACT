import logging
from unittest.mock import patch, Mock
from logging import Logger
import pytest

import yaml
from src.loggerfactory import LoggerFactory


@pytest.fixture
def mock_config_dict():
    return {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "loggers": {
            "test_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
            }
        },
    }


@pytest.fixture
def custom_cfg_path(tmp_path, mock_config_dict):

    # Set up a temporary logging configuration file for the test
    temp_cfg_path = tmp_path / "temporary_logging_config.yml"
    with open(temp_cfg_path, "w+") as fh:
        yaml.dump(mock_config_dict, fh)
    return temp_cfg_path


@patch("src.loggerfactory.logging.config.dictConfig")
def test_logger_factory(mock_dict_config, custom_cfg_path, mock_config_dict):
    # Mock the logger to check if getLogger is called with the correct parameters
    with patch("src.loggerfactory.logging.getLogger", return_value=Mock(spec=Logger)) as mock_get_logger:

        # Define the expected logging configuration dictionary
        expected_config_dictionary = mock_config_dict

        # Call the LoggerFactory to get a logger
        logger = LoggerFactory.get_logger("test_logger", custom_cfg_path)

        # Assert that the logger is obtained correctly
        assert logger == mock_get_logger.return_value

        # Assert that the logging configuration is loaded correctly
        mock_dict_config.assert_called_once_with(expected_config_dictionary)


def test_custom_logger_name():
    # Call LoggerFactory.get_logger with a custom logger name
    logger = LoggerFactory.get_logger("custom_logger")

    # Assert that the logger is obtained with the custom logger name
    assert logger.name == "custom_logger"


def test_multiple_calls_same_logger_name():
    # Call LoggerFactory.get_logger multiple times with the same logger name
    logger1 = LoggerFactory.get_logger("shared_logger")
    logger2 = LoggerFactory.get_logger("shared_logger")

    # Assert that both calls return the same logger instance
    assert logger1 is logger2


def test_different_logger_names():
    # Call LoggerFactory.get_logger with different logger names
    logger1 = LoggerFactory.get_logger("logger1")
    logger2 = LoggerFactory.get_logger("logger2")

    # Assert that the obtained logger instances have different names
    assert logger1.name != logger2.name


def test_logger_handlers(custom_cfg_path):
    # Call LoggerFactory.get_logger with a custom configuration file
    logger = LoggerFactory.get_logger("test_logger", custom_cfg_path)

    # Assert that the logger has the expected handlers configured
    assert any(isinstance(handler, logging.StreamHandler)
               for handler in logger.handlers)


def test_logger_level(custom_cfg_path):
    # Call LoggerFactory.get_logger with a custom configuration file
    logger = LoggerFactory.get_logger(
        "test_logger", cfg_path=custom_cfg_path)

    # Assert that the logger has the expected logging level configured
    assert logger.level == logging.DEBUG
