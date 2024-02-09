from pathlib import Path
from typing import Iterable, List, NamedTuple

import pandas as pd
from src.books import Books
from src.taxpayerportal import TaxPayerPortal
from src.template_file import TemplateFile


class TransactionAbove1L(NamedTuple):
    """
    Represents a transaction above 1L with the following fields:
    - pan_no: PAN number
    - bill_receiveable_person: Name of the person or entity to receive the bill
    - trade_name_type: Type of trade name
    - transaction_type: Type of transaction
    - taxable_amount: Taxable amount
    - exempted_amount: Exempted amount
    """

    pan_no: str
    bill_receiveable_person: str
    trade_name_type: str
    transaction_type: str
    taxable_amount: int
    exempted_amount: int


class LakhBusters:
    """
    Class to manage transactions above 1L and generate reports.
    """

    _lakh_busters: List[TransactionAbove1L] = []

    def __init__(self, work_dir: Path):
        """
        Initialize LakhBusters with the working directory.
        """

        self.book = Books.ONE_LAKH_PLUS.value
        self.buffer = self.get_1L_plus_template_buffer()
        self.save_filepath = work_dir.joinpath("transactions_above_1L.xls")

    def get_1L_plus_template_buffer(self):
        """
        Retrieves the template file for transaction above 1L as a BytesIO buffer.

        Returns:
            A BytesIO object containing the template file's contents.
        """

        template_file = TemplateFile(TaxPayerPortal(), None)

        # Retrieve the template file for the specified book as BytesIO buffer
        template_data = template_file.get(self.book)

        return template_data

    def save(self):
        """
        Write the buffer to lakh_buster's filepath
        """
        headers = pd.read_excel(self.buffer).columns
        df_1L = pd.DataFrame(LakhBusters._lakh_busters, columns=headers)
        df_1L.to_excel(self.save_filepath, index=False)

    @classmethod
    def get_lakh_busters(cls):
        """
        Retrieve the list of lakh busters.
        """
        return cls._lakh_busters

    @classmethod
    def update_lakh_busters(cls, new_lakh_busters: Iterable):
        """
        Update the list of lakh busters with a new list.
        """
        cls._lakh_busters.extend(new_lakh_busters)

    @classmethod
    def reset_busters(cls):
        """
        Reset the list of lakh busters.
        """
        cls._lakh_busters = []
