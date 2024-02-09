from dataclasses import dataclass
from enum import Enum
from typing import List, Literal

from src.loggerfactory import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


class ID(Enum):
    PURCHASE, SALES = range(1, 3)


@dataclass
class BookColumns:
    filter: List[str]


@dataclass
class EmptyColumns:
    indices: List[int]


@dataclass
class Book:
    id: ID
    name: Literal['purchase', 'sales', 'File 1L+']
    sheet: Literal['Nepali PB', 'Nepali SB', 'Sheet1']
    symbol: Literal['P', 'S', '1L']
    columns: BookColumns
    endpoint: str
    emptycols: EmptyColumns


class Books(Enum):
    PURCHASE = Book(
        ID.PURCHASE.value,
        'purchase',
        'Nepali PB',
        'P',
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
        'S',
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
        '1L',
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
