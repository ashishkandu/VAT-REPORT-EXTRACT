import pytest
from src.filingmonth import FilingMonth


class TestFilingMonth:
    """Tests for FilingMonth."""

    def setup_method(self):
        self.filingmonth = FilingMonth(2080, 2)

    def test_get_BS_date_range(self):
        expected_date_range = "2080-02-01 - 2080-02-32"
        bs_date_range = self.filingmonth.get_BS_date_range()
        assert str(bs_date_range) == expected_date_range

    def test_get_AD_date_range(self):
        expected_date_range = "2023-05-15 - 2023-06-15"
        ad_date_range = self.filingmonth.get_AD_date_range()
        assert str(ad_date_range) == expected_date_range

    def test_get_fiscal_year(self):
        expected_fiscal_year = "2079/80"
        fiscal_year = self.filingmonth.get_fiscal_year()
        assert fiscal_year == expected_fiscal_year


class TestFilingMonthError:
    """Tests for FilingMonth which raise error"""

    def test_invalid_type(self) -> None:
        """Test filingMonth object creation with invalid data types."""
        with pytest.raises(TypeError):
            FilingMonth('2080', '12')
