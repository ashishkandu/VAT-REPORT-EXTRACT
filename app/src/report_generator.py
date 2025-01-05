from typing import Optional, Union

from settings import SHEETS_DIR

from src.books import Book, Books
from src.filingmonth import FilingMonth
from src.one_lakh_plus_transactions import LakhBusters
from src.report import Report


class ReportGenerator:
    """
    Generates report based on the given filing month and book. If book is None, reports are generated for all purchase and sales books.
    Also, updates lakh_busters with the transactions above 1L.
    """

    def __init__(self, filingMonth: FilingMonth):
        self.filingMonth = filingMonth
        self.work_dir = SHEETS_DIR.joinpath(
            self.filingMonth.get_fiscal_year().replace("/", "-"),
            self.filingMonth.nepali_month_name(),
        )
        self._lakh_busters: Optional[LakhBusters] = None

    @property
    def lakh_busters(self) -> LakhBusters:
        """
        Getter method for accessing the LakhBusters instance. If the instance does not exist, it is created using the work directory.
        """
        if self._lakh_busters is None:
            self._lakh_busters = LakhBusters(self.work_dir)
            self._lakh_busters.reset_busters()
        return self._lakh_busters

    def generate(self, book: Union[Book, None]) -> None:
        """
        Generate report for the given book and update lakh_busters if generating for multiple books.

        Parameters:
            book (Union[Book, None]): The book for which the report is generated. If None, reports are generated for all purchase and sales books.

        Returns:
            None
        """
        if book is None:
            books = (Books.SALES.value, Books.PURCHASE.value)
        else:
            books = (book,)
        for selected_book in books:
            report = self.get_report(selected_book)

            # Only use lakh_busters if generating for multiple books
            if book is None:
                transactions_above_1L = report.get_transactions_above_1L()
                self.lakh_busters.update_lakh_busters(transactions_above_1L)

            self._generate_report_outputs(report)

        # Only save lakh_busters if generating for multiple books
        if book is None:
            self.lakh_busters.save()

    def _generate_report_outputs(self, report: Report) -> None:
        """
        Generate the report outputs and save the report.
        :param report: The report object to generate outputs for.
        :return: None
        """
        report.save()
        # report.print_cancelled_transactions()
        report.print_transactions_with_roundoff()
        report.print_transactions_summary()

    def get_report(self, book: Book) -> Report:
        """
        Get a report based on the given book and return it.

        Args:
            self: The object itself.
            book (Book): The book to generate the report from.

        Returns:
            Report: The report reposrenting the given book.
        """
        return Report(book, self.filingMonth, self.work_dir)
