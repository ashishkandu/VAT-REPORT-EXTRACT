import os
import pytest
from unittest.mock import patch

from src.db_connection import DB_CONFIGURATION_PATH, SQLEngine


@pytest.fixture
def mock_config_data():
    mock_config_data = {
        'driver': {'name': 'mock_driver'},
        'server': {'name': 'mock_server'},
        'database': {'name': 'mock_database'},
        'user': {'name': 'mock_user'}
    }
    return mock_config_data


# def test_db_config_exists():
#     assert DB_CONFIGURATION_PATH.exists()


# @patch('os.getenv')
# @patch('tomli.load')
# def test_connection_string_creation(mock_toml_load, mock_getenv, mock_config_data):

#     mock_toml_load.return_value = mock_config_data
#     mock_getenv.return_value = 'test_password'

#     connection_string = SQLEngine.get()

#     expected_string = f"DRIVER={{{mock_config_data['driver']['name']}}};SERVER={mock_config_data['server']['name']};DATABASE={mock_config_data['database']['name']};UID={mock_config_data['user']['name']};PWD={mock_getenv.return_value}"
#     assert connection_string.url.query['odbc_connect'] == expected_string


# @patch('tomli.load')
# def test_config_loading(mock_toml_load, mock_config_data):

#     mock_toml_load.return_value = mock_config_data

#     with patch.dict(os.environ, {"SA_PASSWORD": "asdf"}):
#         SQLEngine.get()  # Call the function to trigger loading

#     mock_toml_load.assert_called_once()

# @patch('src.db_connection.create_engine')
# def test_engine_creation(mock_create_engine):
#     SQLEngine.get()

#     mock_create_engine.assert_called_once()

class TestSQLEngine:
    
    def teardown_method(self, method):
        SQLEngine.reset()

    @patch('os.getenv')
    @patch('tomli.load')
    def test_load_db_configurations(self, mock_tomli_load, mock_getenv, mock_config_data):
        """Successfully load DB configurations from config file"""
        
        # Use mock tomli.load function to return a mock config data
        mock_tomli_load.return_value = mock_config_data

        # Use mock os.getenv function to return a mock password
        mock_getenv.return_value = 'mock_password'

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None

    def test_get_sql_engine_instance(self, mocker, mock_config_data):
        """Successfully get SQL engine instance"""
        
        # Mock the tomli.load function to return a mock config data
        mock_tomli_load = mocker.patch('tomli.load')
        mock_tomli_load.return_value = mock_config_data

        # Mock the os.getenv function to return a mock password
        mock_getenv = mocker.patch('os.getenv')
        mock_getenv.return_value = 'mock_password'

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None

    def test_sql_engine_singleton(self, mocker, mock_config_data):
        """SQL engine instance is a singleton"""
        
        # Mock the tomli.load function to return a mock config data
        mock_tomli_load = mocker.patch('tomli.load')
        mock_tomli_load.return_value = mock_config_data

        # Mock the os.getenv function to return a mock password
        mock_getenv = mocker.patch('os.getenv')
        mock_getenv.return_value = 'mock_password'

        # Call the get method of SQLEngine twice
        sql_engine_1 = SQLEngine.get()
        sql_engine_2 = SQLEngine.get()

        # Assert that the tomli.load function was called only once
        mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called only once
        mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine instances are the same
        assert sql_engine_1 is sql_engine_2

    
    def test_retrieve_password_from_env_variable(self, mocker, mock_config_data):
        """Password is retrieved from environment variable"""
        
        # Mock the tomli.load function to return a mock config data
        mock_tomli_load = mocker.patch('tomli.load')
        mock_tomli_load.return_value = mock_config_data

        # Mock the os.getenv function to return a mock password
        mock_getenv = mocker.patch('os.getenv')
        mock_getenv.return_value = 'mock_password'

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None
        
        