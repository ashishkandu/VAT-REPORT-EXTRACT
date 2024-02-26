import pytest
from unittest.mock import patch

from src.db_connection import SQLEngine


@pytest.fixture
def mock_config_data():
    mock_config_data = {
        'driver': {'name': 'mock_driver'},
        'server': {'name': 'mock_server'},
        'database': {'name': 'mock_database'},
        'user': {'name': 'mock_user'}
    }
    return mock_config_data


class TestSQLEngine:

    def setup_method(self):
        self.mock_config_data = {
            'driver': {'name': 'mock_driver'},
            'server': {'name': 'mock_server'},
            'database': {'name': 'mock_database'},
            'user': {'name': 'mock_user'}
        }
        # Mock the tomli.load function to return a mock config data
        self.mock_tomli_load = patch('tomli.load').start()
        self.mock_tomli_load.return_value = self.mock_config_data
        
        # Mock the os.getenv function to return a mock password
        self.mock_getenv = patch('os.getenv').start()
        self.mock_getenv.return_value = 'mock_password'

    def teardown_method(self, method):
        SQLEngine.reset()    
        patch.stopall()

    def test_load_db_configurations(self):
        """Successfully load DB configurations from config file"""

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None
        
    def test_sql_engine_singleton(self):
        """SQL engine instance is a singleton"""

        # Call the get method of SQLEngine twice
        sql_engine_1 = SQLEngine.get()
        sql_engine_2 = SQLEngine.get()

        # Assert that the tomli.load function was called only once
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called only once
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine instances are the same
        self.assertEqual(sql_engine_1, sql_engine_2)

    def test_load_db_configurations(self):
        """Successfully load DB configurations from config file"""

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None

    def test_get_sql_engine_instance(self):
        """Successfully get SQL engine instance"""

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None

    def test_sql_engine_singleton(self):
        """SQL engine instance is a singleton"""
        
        # Call the get method of SQLEngine twice
        sql_engine_1 = SQLEngine.get()
        sql_engine_2 = SQLEngine.get()

        # Assert that the tomli.load function was called only once
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called only once
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine instances are the same
        assert sql_engine_1 is sql_engine_2

    
    def test_retrieve_password_from_env_variable(self):
        """Password is retrieved from environment variable"""

        # Call the get method of SQLEngine
        sql_engine = SQLEngine.get()

        # Assert that the tomli.load function was called
        self.mock_tomli_load.assert_called_once()

        # Assert that the os.getenv function was called
        self.mock_getenv.assert_called_once_with('SA_PASSWORD')

        # Assert that the SQL engine was returned
        assert sql_engine is not None
        
    
    def test_connection_string_creation(self, mock_config_data):
        
        connection_string = SQLEngine.get()

        expected_string = f"DRIVER={{{mock_config_data['driver']['name']}}};SERVER={mock_config_data['server']['name']};DATABASE={mock_config_data['database']['name']};UID={mock_config_data['user']['name']};PWD={self.mock_getenv.return_value}"
        assert connection_string.url.query['odbc_connect'] == expected_string