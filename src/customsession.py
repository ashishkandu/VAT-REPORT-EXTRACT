from urllib.parse import urljoin

from requests import Session
from requests.adapters import HTTPAdapter, Retry


retry_strategy = Retry(
    total=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
)

adapter = HTTPAdapter(max_retries=retry_strategy)


class CustomSession(Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.mount('http://', adapter)
        self.mount('https://', adapter)

        self.base_url = lambda path: urljoin(base_url, path)
