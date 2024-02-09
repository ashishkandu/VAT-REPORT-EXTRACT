import logging
import pytest


@pytest.fixture(autouse=True)
def disable_logging():
    # Save the original logging configuration
    original_logging_config = logging.getLogger().handlers.copy()

    # Remove all handlers from the root logger to suppress logging during tests
    # logging.getLogger().handlers = []
    # print(logging.getLogger().handlers)

    # Set StreamHandler as the only handler for testing
    logging.getLogger().handlers = [logging.getLogger().handlers.pop(0)]

    # If LoggerFactory has already been initialized, replace its handlers as well
    # if LoggerFactory._LOG:
    #     LoggerFactory._LOG.handlers = []

    yield

    # Restore the original logging configuration after the tests
    logging.getLogger().handlers = original_logging_config
