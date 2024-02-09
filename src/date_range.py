from dataclasses import dataclass
from datetime import date
from pyBSDate import bsdate


@dataclass
class BSDateRange:
    """Represents a date range in Bikram Sambat (BS) format."""
    start: bsdate
    end: bsdate

    def __str__(self) -> str:
        """Returns a string representation of the date range."""
        return f"{self.start} - {self.end}"


@dataclass
class ADDateRange:
    """Represents a date range in Anno Domini (AD) format."""
    start: date
    end: date

    def __str__(self) -> str:
        """Returns a string representation of the date range."""
        return f"{self.start} - {self.end}"
