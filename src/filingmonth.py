from datetime import date
import nepali_datetime
from pyBSDate import bsdate
from pyBSDate.DateConverter import _bs_to_ad

from src.date_helpers import get_month_name_np
from src.date_range import ADDateRange, BSDateRange


class FilingMonth:
    """
        FilingMonth represents the nepali month for which VAT reports
        will be prepared.

        Args:
            year (int): Year according to Nepali Calander.
            month (int): Month according to Nepali Calander.
    """

    def __init__(self, year: int, month: int):

        if not (isinstance(year, int) and isinstance(month, int)):
            raise TypeError('Please provide year and month as int')
        self.year = year
        self.month = month
        self.name = get_month_name_np(self.month)
        # self.bs_date_range = self.get_BS_date_range()
        # self.ad_date_range = self.get_AD_date_range(self.bs_date_range)

    @staticmethod
    def __convert_BS_to_AD(bs_date: bsdate):
        """It is a conversion funcion to convert the BS date to standard AD date"""
        return date(*_bs_to_ad(bs_date.year, bs_date.month, bs_date.day))

    def get_BS_date_range(self) -> BSDateRange:
        """
        Returns date range for the BS month in BS format
        """
        last_day = nepali_datetime._days_in_month(
            year=self.year, month=self.month)
        return BSDateRange(
            bsdate(year=self.year, month=self.month, day=1),
            bsdate(year=self.year, month=self.month, day=last_day)
        )

    def get_AD_date_range(self) -> ADDateRange:
        """
        Returns date range in AD format
        """
        bs_date_range = self.get_BS_date_range()
        start_conv = FilingMonth.__convert_BS_to_AD(bs_date_range.start)
        end_conv = FilingMonth.__convert_BS_to_AD(bs_date_range.end)
        return ADDateRange(start=start_conv, end=end_conv)

    def get_fiscal_year(self) -> str:
        """Returns the fiscal year as provided year and month."""
        if self.month > 3:
            fiscal_year = f'{self.year}/{str(self.year+1)[2:]}'
        else:
            fiscal_year = f'{self.year-1}/{str(self.year)[2:]}'
        return fiscal_year

    def nepali_month_name(self) -> str:
        """Returns the month name as per nepali calander for this filing month."""
        return get_month_name_np(self.month)
