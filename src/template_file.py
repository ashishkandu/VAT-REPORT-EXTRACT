import hashlib
from io import BytesIO
from typing import Literal
from settings import DOWNLOAD, HASH_VALUE, TEMPLATE_SAVE_DIR
from src.books import Book
from src.cbms import TokenAuth
from src.customsession import CustomSession
from src.file_handlers import write_bytes_to_disk
from src.loggerfactory import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


class TemplateFile:
    """To work with custom sessions for standard files. Downloader."""

    def __init__(self, session: CustomSession, token_auth: TokenAuth):
        self.session = session
        self.token_auth = token_auth

    def get(self, book: Book) -> BytesIO:
        """Download the format file from CBMS and return in bytes."""
        self.session.headers.update(
            {'Content-Disposition': 'attachment; filename=template.xlsx'})
        response = self.session.get(self.session.base_url(
            book.endpoint), auth=self.token_auth)
        logger.info(
            f"{response.request.method} {response.url} [status:{response.status_code} request:{response.elapsed.total_seconds():.3f}s]")
        response.raise_for_status()
        cache_hash = self.get_hash_value(book.name)
        if not self.__validate_bytes(response.content, cache_hash):
            raise Exception('Error validating the file against its MD5 hash')
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
        return buffer

    def get_hash_value(self, book_name: Literal["purchase", "sales", "File 1L+"]) -> str:
        """Returns hash value for the respective book or raise ValueError"""

        try:
            return HASH_VALUE[book_name]
        except KeyError:
            raise ValueError(
                "Please check HASH_VALUE in configurations settings")

    def __validate_bytes(self, content: bytes, hash: str):
        """
        Validates downloaded content in bytes with an md5 hash value
        Args:
            content (bytes): file downloaded in :obj:`bytes` form
            hash (str): hash value to compare
        """
        m = hashlib.md5(content)
        return m.hexdigest() == hash
