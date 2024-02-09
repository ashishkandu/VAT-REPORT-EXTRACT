from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from src.configurations import get_data


def test_get_data_file_not_found() -> None:
    """
    Test get_data function with invalid path for
    loading runtime configurations.
    """
    with pytest.raises(FileNotFoundError):
        get_data("abc", Path("Invalid/path"))


def test_get_data_inavlid_key() -> None:
    """
    Test get_data function with invalid key for
    loading runtime configurations.
    """
    with pytest.raises(SystemExit):
        get_data("NONEXISTINGKEY")


def test_get_data_success(tmp_path) -> None:
    """
    Test get_data function and match the key details.
    """

    # Using tmp_path to create a temporary directory
    temp_dir = tmp_path / "config_dir"
    temp_dir.mkdir()

    test_details = {
        "details": {
            "PAN": 123456789,
            "office_name": "XYZ STORES"
        }
    }
    # Creation of a tmp_runtime_config.yml file
    temp_config_file = temp_dir / "temp_runtime_config.yml"
    with open(temp_config_file, "w+") as fh:
        yaml.dump(test_details, fh)

    details = get_data("details", temp_config_file)
    assert details == test_details["details"]


def test_get_data_key_error():
    with patch('yaml.safe_load', return_value={"key1": "value1"}):
        with pytest.raises(SystemExit):
            get_data("key2")


def test_get_data_yaml_error():
    with patch('yaml.safe_load', side_effect=yaml.YAMLError("Invalid YAML")):
        with pytest.raises(SystemExit):
            get_data("some_key")
