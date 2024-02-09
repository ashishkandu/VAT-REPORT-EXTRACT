from io import BytesIO
from unittest.mock import mock_open, patch
from src.file_handlers import write_bytes_to_disk


def test_write_bytes_to_disk(tmp_path) -> None:
    """
    It tests writing of bytes data to a system extension file
    e.g., txt
    """
    buffer_content = b'Test content'
    buffer = BytesIO(buffer_content)

    filepath = tmp_path / 'test_file.txt'

    with patch('builtins.open', mock_open()) as mock_file:
        write_bytes_to_disk(buffer, filepath)

    mock_file.assert_called_once_with(filepath, 'wb')
    mock_file().write.assert_called_once_with(buffer_content)
