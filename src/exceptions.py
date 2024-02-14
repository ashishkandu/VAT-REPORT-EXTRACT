class FileValidationError(Exception):
    """Raised when the file validation against its MD5 hash fails."""
    pass


class BookNameNotFoundError(Exception):
    """Raised when the book name is not found in HASH_VALUE."""
    pass
