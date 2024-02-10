import pytest
from io import BytesIO
from src.file_handlers import write_bytes_to_disk


class TestWriteBytesToDisk:

    # Writes bytes data to a system extension file.
    def test_write_bytes_to_disk_writes_data_to_file(self, tmp_path):
        buffer_content = b'Test content'
        buffer = BytesIO(buffer_content)
        filepath = tmp_path / 'test_file.txt'
        write_bytes_to_disk(buffer, filepath)
        assert filepath.read_bytes() == buffer_content

    # Logs the action and completion of the write operation.
    def test_write_bytes_to_disk_logs_action_and_completion(self, tmp_path, caplog):
        buffer_content = b'Test content'
        buffer = BytesIO(buffer_content)
        filepath = tmp_path / 'test_file.txt'
        write_bytes_to_disk(buffer, filepath)
        assert f'Saving contents to {filepath.name}' in caplog.text
        assert 'File write completed!' in caplog.text

    # Creates parent directories if they do not exist.
    def test_write_bytes_to_disk_creates_parent_directories(self, tmp_path):
        buffer_content = b'Test content'
        buffer = BytesIO(buffer_content)
        filepath = tmp_path / 'parent_dir' / 'test_file.txt'
        write_bytes_to_disk(buffer, filepath)
        assert filepath.exists()

    # Raises PermissionError if there is an error writing to the file.
    def test_write_bytes_to_disk_raises_permission_error(self, tmp_path):
        buffer_content = b'Test content'
        buffer = BytesIO(buffer_content)
        filepath = tmp_path / 'test_file.txt'
        # Set the file to read-only
        filepath.touch(mode=0o444)
        with pytest.raises(PermissionError):
            write_bytes_to_disk(buffer, filepath)

    # Handles writing to the file with no errors.
    def test_write_bytes_to_disk_no_errors(self, tmp_path):
        buffer_content = b'Test content'
        buffer = BytesIO(buffer_content)
        filepath = tmp_path / 'test_file.txt'
        write_bytes_to_disk(buffer, filepath)
