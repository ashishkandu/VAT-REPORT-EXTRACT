import os
import pytest
from unittest.mock import patch

from src.db_connection import DB_CONFIGURATION_PATH, get_sql_engine


@pytest.fixture
def mock_config_data():
    mock_config_data = {
        'driver': {'name': 'test_driver'},
        'server': {'name': 'test_server'},
        'database': {'name': 'test_dB'},
        'user': {'name': 'test_user'},
    }
    return mock_config_data


def test_db_config_exists():
    assert DB_CONFIGURATION_PATH.exists()


@patch('tomli.load')
def test_config_loading(mock_toml_load, mock_config_data):

    mock_toml_load.return_value = mock_config_data

    with patch.dict(os.environ, {"DBpassword": "asdf"}):
        get_sql_engine()  # Call the function to trigger loading

    mock_toml_load.assert_called_once()


@patch('os.getenv')
def test_env_var_loading(mock_getenv):
    mock_getenv.return_value = 'test_password'

    get_sql_engine()

    mock_getenv.assert_called_once_with('SA_PASSWORD')


@patch('os.getenv', return_value=None)
def test_missing_password(mock_getenv):
    with pytest.raises(SystemExit):
        get_sql_engine()


@patch('os.getenv')
@patch('tomli.load')
def test_connection_string_creation(mock_toml_load, mock_getenv, mock_config_data):

    mock_toml_load.return_value = mock_config_data
    mock_getenv.return_value = 'test_password'

    connection_string = get_sql_engine()

    expected_string = f"DRIVER={{{mock_config_data['driver']['name']}}};SERVER={mock_config_data['server']['name']};DATABASE={mock_config_data['database']['name']};UID={mock_config_data['user']['name']};PWD={mock_getenv.return_value}"
    assert connection_string.url.query['odbc_connect'] == expected_string


@patch('src.db_connection.create_engine')
def test_engine_creation(mock_create_engine):
    get_sql_engine()

    mock_create_engine.assert_called_once()
