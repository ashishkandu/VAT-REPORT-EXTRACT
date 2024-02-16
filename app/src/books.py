from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Literal

from src.loggerfactory import LoggerFactory


# Get the logger for the current module
logger = LoggerFactory.get_logger(__name__)


class ID(Enum):
    """
    Enumeration for book IDs.
    """
    PURCHASE = 1  # Represents the ID for the 'PURCHASE' book.

    SALES = 2  # Represents the ID for the 'SALES' book.

    @classmethod
    def list(cls):
        """
        Returns a list of values obtained by mapping the 'value' attribute of each instance of the class.
        """
        return list(map(lambda x: x.value, cls))


@dataclass
class BookColumns:
    """
    Dataclass representing the columns of a book.
    """
    column_names: List[str]


@dataclass
class EmptyColumns:
    """
    Dataclass representing the empty columns of a book.
    """
    indices: Set[int]


@dataclass
class Book:
    """
    Dataclass representing a book.
    """
    id: ID
    name: Literal['purchase', 'sales', 'File 1L+']
    sheet: Literal['Nepali PB', 'Nepali SB', 'Sheet1']
    # symbol: Literal['P', 'S', '1L']
    columns: BookColumns
    endpoint: str
    emptycols: EmptyColumns

    @property
    def symbol(self) -> Literal['P', 'S', '1L']:
        """
        Property representing the symbol of the book.
        """
        if self.name == 'purchase':
            return 'P'
        elif self.name == 'sales':
            return 'S'
        elif self.name == 'File 1L+':
            return '1L'
        else:
            raise ValueError("Invalid book name")


class Books(Enum):
    """
    Enumeration for different types of books.
    """
    PURCHASE = Book(
        ID.PURCHASE.value,
        'purchase',
        'Nepali PB',
        BookColumns([
            'Nepali Date',
            'Reference No',
            'Bill Receiveable Person',
            'Vat Pan No',
            # 'Item',
            # 'In',
            # 'Symbol',
            'Grand Total',
            'Taxable Amount',
            'Tax Amount',
        ]),
        '/api/billingregister/BillingRegister/excelFile/2',
        EmptyColumns([2, 6]),
    )
    SALES = Book(
        ID.SALES.value,
        'sales',
        'Nepali SB',
        BookColumns([
            'Nepali Date',
            'Transaction ID',
            'Bill Receiveable Person',
            'Vat Pan No',
            # 'Item',
            # 'Out',
            # 'Symbol',
            'Grand Total',
            'Taxable Amount',
            'Tax Amount',
        ]),
        '/api/billingregister/BillingRegister/excelFile/1',
        EmptyColumns([5]),
    )
    ONE_LAKH_PLUS = Book(
        0,
        'File 1L+',
        'Sheet1',
        BookColumns([]),
        'Sample%20Files/Transaction%20Above%20One%20Lakh%20Sample%20Document.xls',
        EmptyColumns([]),
    )

    @classmethod
    def list(cls):
        """
        Returns a list of values obtained by mapping the 'value' attribute of each instance of the class.
        """
        return list(map(lambda x: x.value, cls))
