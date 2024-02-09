from dataclasses import dataclass
from datetime import date
from pyBSDate import bsdate


@dataclass
class BSDateRange:
    """Represents start date and end date in BS format"""
    start: bsdate
    end: bsdate

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"


@dataclass
class ADDateRange:
    """Represents start date and end date in AD format"""
    start: date
    end: date

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"
