import hashlib
from io import BytesIO
from typing import Literal
from settings import DOWNLOAD, HASH_VALUE, TEMPLATE_SAVE_DIR
from src.books import Book
from src.cbms import TokenAuth
from src.customsession import CustomSession
from src.exceptions import BookNameNotFoundError, FileValidationError
from src.file_handlers import write_bytes_to_disk
from src.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)


class TemplateFile:
    """To work with custom sessions for standard files. Downloader."""

    def __init__(self, session: CustomSession, token_auth: TokenAuth):
        """
        Initialize TemplateFile with the given session and token authentication.

        Args:
            session (CustomSession): The custom session to be used for downloading files.
            token_auth (TokenAuth): The token authentication to be used for the session.
        """
        self.session = session
        self.token_auth = token_auth

    def get(self, book: Book) -> BytesIO:
        """
        Download the format file from CBMS and return in bytes.

        Args:
            book (Book): The book object representing the file to be downloaded.

        Returns:
            BytesIO: The downloaded file in bytes.

        Raises:
            Exception: If there is an error validating the file against its MD5 hash.
        """
        self.session.headers.update(
            {'Content-Disposition': 'attachment; filename=template.xlsx'})
        response = self.session.get(self.session.base_url(
            book.endpoint), auth=self.token_auth)
        logger.info(
            f"{response.request.method} {response.url} [status:{response.status_code} request:{response.elapsed.total_seconds():.3f}s]")
        response.raise_for_status()
        cache_hash = self.get_hash_value(book.name)
        buffer = BytesIO(response.content)

        if DOWNLOAD:
            # d = response.headers['content-disposition']
            # filename: str = re.findall("filename=(.+)", d)[0]
            # filename = filename.split(';')[0]
            logger.info(
                f"Downloading {book.name} to local, check settings.py for options.")
            filename = f"{book.name}.xlsx"
            if book.name == "File 1L+":
                filename = f"{book.name}.xls"

            TEMPLATE_SAVE_DIR.mkdir(parents=True, exist_ok=True)
            filepath = TEMPLATE_SAVE_DIR / filename
            write_bytes_to_disk(buffer, filepath)
        if not self.__validate_bytes(buffer.getvalue(), cache_hash):
            raise FileValidationError(
                f'Error validating the file against its MD5 hash. Expected: {cache_hash}, Got: {self.computed_hash}')
        return buffer

    def get_hash_value(self, book_name: Literal["purchase", "sales", "File 1L+"]) -> str:
        """
        Returns hash value for the respective book or raise ValueError

        Args:
            book_name (Literal["purchase", "sales", "File 1L+"]): The name of the book for which the hash value is required.

        Returns:
            str: The hash value for the specified book.

        Raises:
            ValueError: If the book name is not found in HASH_VALUE in configurations settings.
        """
        try:
            return HASH_VALUE[book_name]
        except KeyError:
            raise BookNameNotFoundError(
                "Please check HASH_VALUE in configurations settings")

    def __validate_bytes(self, content: bytes, hash: str):
        """
        Validates downloaded content in bytes with an md5 hash value

        Args:
            content (bytes): The file downloaded in :obj:`bytes` form.
            hash (str): The hash value to compare.

        Returns:
            bool: True if the hash value matches, False otherwise.
        """
        self.computed_hash = hashlib.md5(content).hexdigest()
        return self.computed_hash == hash
