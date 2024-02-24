from io import BytesIO
from pathlib import Path
from typing import List
from openpyxl import load_workbook
import pandas as pd
from src.books import Book
from src.cbms import CBMS, TokenAuth

from src.configurations import get_data
from src.db_connection import get_sql_engine
from src.file_handlers import write_bytes_to_disk
from src.filingmonth import FilingMonth
from src.loggerfactory import LoggerFactory
from src.one_lakh_plus_transactions import TransactionAbove1L
from src.template_file import TemplateFile


logger = LoggerFactory.get_logger(__name__)


class Report:
    def __init__(self, book: Book, filing_month: FilingMonth, work_dir: Path):
        """
        Initialize the object with the provided book, filing month, and work directory.

        Args:
            book (Book): The book to be initialized with.
            filing_month (FilingMonth): The filing month to be initialized with.
            work_dir (Path): The work directory to be initialized with.
        """
        self.book = book

        self.filing_month = filing_month
        self.filing_month_name = self.filing_month.nepali_month_name()
        self.date_range = self.filing_month.get_AD_date_range()
        self.save_filepath = work_dir.joinpath(
            f"{self.book.name} - {self.filing_month_name}.xlsx")

        self.cancelled_transactions = []
        self.buffer = BytesIO()

        self._raw_transactions = None
        self._transactions = None

    @property
    def raw_transactions(self) -> pd.DataFrame:
        """
        Property to lazily load raw transactions from the database.

        Returns:
        pd.DataFrame: The raw transactions data.
        """
        if self._raw_transactions is None:
            self._raw_transactions = self.query_db()
        return self._raw_transactions

    @property
    def transactions(self) -> pd.DataFrame:
        """
        Property method to access transactions data.

        Returns:
        pd.DataFrame: The transactions data.
        """
        if self._transactions is None:
            self._transactions = self.process_transactions()
        return self._transactions

    def query_db(self) -> pd.DataFrame:
        """
        Queries the database and returns the results as a pandas DataFrame.

        Args:
            self: The instance of the class containing the query parameters.

        Returns:
            A pandas DataFrame containing the query results.
        """

        # Retrieve the SQL query string from toml file
        sql_query = get_data('sql')

        # Get a SQLAlchemy engine instance for database interaction
        engine = get_sql_engine()

        logger.info("Querying database...")

        # Execute the SQL query and return the results as a DataFrame
        dataframe = pd.read_sql(
            sql_query,  # The SQL query string
            engine,  # The SQLAlchemy engine
            params=(
                self.book.id,  # Bind the book ID as a parameter
                self.date_range.start,  # Bind the start date as a parameter
                self.date_range.end  # Bind the end date as a parameter
            )
        )

        # A post processing to remove cancelled transactions
        return self.remove_cancelled_transactions(dataframe)

    def process_transactions(self) -> pd.DataFrame:
        """
        Filters and processes transactions to match the book format,
        returning a DataFrame ready for template filling.

        Args:
            self: The instance of the class containing the transaction data.

        Returns:
            A DataFrame with filtered columns, empty columns for fitting,
            and temporary numeric conversion for missing PANs.
        """

        # Filter the DataFrame to keep only the columns specified in the book filter
        df = self.raw_transactions.loc[:, self.book.columns.column_names]

        # Reshape for fitting:
        # Insert empty columns at specified indices to match the template structure
        for index in self.book.emptycols.indices:
            df.insert(index, index, None)

        # Handling missing PANs:
        # Temporarily convert empty PANs to numeric 000 for compatibility
        df['Vat Pan No'] = df['Vat Pan No'].mask(df['Vat Pan No'] == '', 000)
        df['Vat Pan No'] = df['Vat Pan No'].astype(int)

        # Restore empty PANs as empty strings after numeric processing
        df['Vat Pan No'] = df['Vat Pan No'].mask(df['Vat Pan No'] == 000, '')

        return df

    def process_cancelled_transactions(self, dataframe: pd.DataFrame):
        """Modify cancelled tranaction's amounts to '-'"""
        amount_columns = ['Grand Total', 'Total w Round',
                          'Taxable Amount', 'Tax Amount']
        for index, row in dataframe.iterrows():
            if row['Status'] == '001-03':
                for col in amount_columns:
                    dataframe.loc[index, col] = '-'
                logger.warning(
                    f"Transaction {row['Transaction ID']} status is: {row['Modify Type']}")
                self.cancelled_transactions.append(row['Transaction ID'])
        return dataframe

    def remove_cancelled_transactions(self, dataframe: pd.DataFrame):
        """Delete cancelled tranactions based on its Status is equal to '001-03'"""
        deleted_indices = []
        for index, row in dataframe.iterrows():
            if row['Status'] == '001-03':
                deleted_indices.append(index)
                logger.warning(
                    f"Transaction {row['Transaction ID']} status is: {row['Modify Type']}")
                logger.info(f"Row {index + 1} was deleted sucessfully!")
                self.cancelled_transactions.append(row['Transaction ID'])
        return dataframe.drop(deleted_indices)

    def get_template_buffer(self):
        """
        Retrieves the template file for the specified book as a BytesIO buffer.

        Args:
            self: The instance of the class containing the book information.

        Returns:
            A BytesIO object containing the template file's contents.
        """

        template_file = TemplateFile(CBMS(), TokenAuth())

        # Retrieve the template file for the specified book as BytesIO buffer
        template_data = template_file.get(self.book)

        return template_data

    def fill_report_details(self) -> None:
        """
        Fills in report details (PAN no., filing year, month, etc.) in the template buffer.

        Args:
            self: The instance of the class containing the report data.
        """

        # Get necessary report details
        data = get_data('details')

        # Construct the detail string using formatted placeholders
        detail = u'करदाता दर्ता नं (PAN) : {}        करदाताको नाम: {}         साल: {}    कर अवधि: {}'.format(
            data['PAN'], data['office_name'], self.filing_month.year, self.filing_month_name)

        # Load the template buffer from its path
        template_buffer = self.get_template_buffer()
        workbook = load_workbook(template_buffer)
        sheet = workbook.active  # Access the active sheet

        # Write the detail string to cell A4
        sheet["A4"] = detail

        # Save the modified workbook to the report buffer
        workbook.save(self.buffer)

    def populate_report_buffer(self) -> None:
        """
        Populates the report buffer with transaction data, building upon existing content.

        Args:
            self: The instance of the class containing the report data.
        """

        # Fill in any necessary report details (e.g., PAN no., filing year)
        self.fill_report_details()

        # Read existing content from the buffer to determine the starting row for appending
        # Use openpyxl for compatibility
        reader = pd.read_excel(self.buffer, engine='openpyxl')

        # Open the buffer in append mode, using openpyxl for compatibility and allowing sheet overlay
        with pd.ExcelWriter(
            self.buffer,
            mode='a',
            engine='openpyxl',
            if_sheet_exists='overlay',  # Overlay existing sheet with the same name
        ) as writer:

            # Write the transaction data to the specified sheet, starting after the existing content
            self.transactions.to_excel(
                writer,
                index=False,  # Exclude the DataFrame index
                header=False,  # Exclude column headers
                sheet_name=self.book.sheet,  # Use the sheet name from the book object
                startrow=len(reader) + 1  # Begin appending after existing rows
            )

    def save(self):
        """
        It populates the report buffer with filtered and processed
        transactions and write the buffer to report's filepath
        """
        self.populate_report_buffer()
        write_bytes_to_disk(self.buffer, self.save_filepath)

    def get_transactions_above_1L(self) -> List[TransactionAbove1L]:
        """
        Aggregate transactions based on PAN Value and return a list of
        transactions with 'Taxable Amount' above 1 lakh, represented as TransactionAbove1L objects.

        Args:
            self: The instance of the class containing the transactions data.

        Returns:
            A list of TransactionAbove1L objects, each representing a transaction with:
            - Vat Pan No
            - Bill Receiveable Person
            - 'E' (purpose unknown, add a comment if possible)
            - Book symbol
            - Taxable Amount
            - 0 (purpose unknown, add a comment if possible)
        """

        # Initialize an empty list to store filtered transactions
        transactions_above_1L = []

        # Filter transactions with a valid 'Vat Pan No' (non-empty strings)
        transactions_PAN = self.transactions[
            self.transactions['Vat Pan No'].astype(bool)
        ]

        # Group transactions by 'Vat Pan No' and aggregate relevant information
        transactions_PAN = transactions_PAN.groupby('Vat Pan No').agg({
            'Bill Receiveable Person': 'first',  # Keep the first 'Bill Receiveable Person'
            'Taxable Amount': 'sum',  # Sum the 'Taxable Amount' for each PAN
            'Grand Total': 'sum',  # Sum the 'Grand Total' for each PAN
        }).reset_index()

        # Filter transactions where 'Grand Total' is above 1,00,000
        transactions_PAN = transactions_PAN[
            transactions_PAN['Grand Total'].gt(1_00_000)
        ].reset_index()

        # The resulting 'transactions_PAN' DataFrame contains aggregated transactions
        # with 'Taxable Amount' above 1,00,000 for each unique 'Vat Pan No'.

        # Iterate through the filtered transactions and construct the output DataFrame:
        for _, row in transactions_PAN.iterrows():
            transactions_above_1L.append(TransactionAbove1L(
                row['Vat Pan No'],
                row['Bill Receiveable Person'],
                'E',
                self.book.symbol,
                row['Taxable Amount'],
                0
            ))

        return transactions_above_1L

    def print_cancelled_transactions(self):
        """
        Prints a formatted list of cancelled transactions to the console.
        """
        if self.cancelled_transactions:
            # Print a heading for the list
            print(f"\nCancelled {self.book.name} transactions:")
            for transaction in self.cancelled_transactions:
                print(f"- {transaction}")

    def print_transactions_with_roundoff(self):
        """
        Compares 'Grand Total' and 'Total w Round' columns in a DataFrame and
        prints only transactions where there is difference.
        """
        df = self.raw_transactions
        transactions_w_roundoff = df.loc[df['Grand Total']
                                         != df['Total w Round']]
        if not transactions_w_roundoff.empty:
            columns = ['Transaction ID', 'Grand Total',
                       'Total w Round', 'Round Off']
            transactions_w_roundoff = transactions_w_roundoff.loc[:, columns]
            # transactions_w_roundoff.loc['Column_Total'] = transactions_w_roundoff.sum(
            #     numeric_only=True, axis=0)
            print(
                f"\n[!] {self.book.name.capitalize()} transactions with round off difference:\n")
            print(transactions_w_roundoff.to_string(index=False))

    def print_transactions_summary(self):
        """
        Prints a summary of the transactions in the report.
        """
        df = self.transactions
        grand_total_sum = df['Grand Total'].sum()
        taxable_amount_sum = df['Taxable Amount'].sum()
        tax_amount_sum = df['Tax Amount'].sum()
        total_transactions = len(df)

        print(f"\n[+] {self.book.name.capitalize()} transactions Summary:\n")
        self.print_cancelled_transactions()
        print(f"Grand Total Sum: {grand_total_sum}")
        print(f"Taxable Amount Sum: {taxable_amount_sum}")
        print(f"Tax Amount Sum: {tax_amount_sum}")
        print(f"Total Transactions: {total_transactions}")
