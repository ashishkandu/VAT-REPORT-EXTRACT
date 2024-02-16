from src.customsession import CustomSession

BASE_URL = 'https://taxpayerportal.ird.gov.np'


class TaxPayerPortal(CustomSession):
    """Custom session optimized to connect to the TaxPayer portal."""

    def __init__(self):
        """Initializes the custom session optimized to connect to the TaxPayer portal."""
        super().__init__(BASE_URL)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
