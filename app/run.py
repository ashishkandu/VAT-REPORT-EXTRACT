import json
from nepali_datetime import datetime as np_datetime
from drive_database.credential_handler import get_cached_credentials
from drive_database.database_operations import restore
from settings import DRIVE_CACHE_PATH, TOKEN_PATH
from drive_database.drive import GoogleDriveFile, download_drive_file, retrive_latest_file_by_pattern
from src.date_helpers import get_month_name_np
from src.filingmonth import FilingMonth
from src.menu import Menu, MenuOption, ReportMenu
from src.nepalidateselector import NepaliDateSelector
from src.report_generator import ReportGenerator


def perform_restore(file: GoogleDriveFile, creds) -> None:
    if DRIVE_CACHE_PATH.exists():
        with DRIVE_CACHE_PATH.open('r') as f:
            info: dict = json.load(f)
        if info['name'] == file['name']:
            print("Database already restored from the latest backup!")
            return None
        else:
            print(
                f"Database was restored from another backup on {info['datetime']}")
            print(f"Current backup: {info['name']}")
            print(f"Latest backup: {file['name']}")
            choice = input("Do you want to restore latest backup? [y/N] ")
            if choice.lower() != 'y':
                return None
            print("Database will be restored from the latest backup!")

    filepath = download_drive_file(creds, file)
    restore(filepath)


def get_month_report(**kwargs) -> None:
    """
    Retrieves the report for the specified month.

    Args:
    **kwargs: additional keyword arguments for month and year

    Returns:
    None
    """
    # Extract month and year from kwargs
    month = kwargs.get("month")
    year = kwargs.get("year")

    # Create FilingMonth instance
    filingmonth = FilingMonth(year=year, month=month)

    # Prompt user for book selection
    report_menu = ReportMenu()
    book = report_menu.prompt_user_for_book()

    # Generate report using ReportGenerator
    report_generator = ReportGenerator(filingMonth=filingmonth)
    report_generator.generate(book)


def get_report_for_another_month() -> None:
    """Retrieves the report for another month."""
    selector = NepaliDateSelector()
    year, month = selector.get_year_month()

    # Call get_month_report with the year and month
    get_month_report(year=year, month=month)


def select_custom_date_range() -> None:
    """
    This function allows the user to select a custom date range for analysis.
    """
    # TODO: Implement the logic for selecting a custom date range
    raise NotImplementedError


if __name__ == "__main__":

    file_pattern = r"VatBillingSoftware_\d+_\d+\.bak"

    # Check if token file exists
    if TOKEN_PATH.exists():
        creds = get_cached_credentials()
    else:
        raise FileNotFoundError(f'Token file not found: {TOKEN_PATH}')

    latest_file = retrive_latest_file_by_pattern(creds, file_pattern)

    if latest_file is not None:
        perform_restore(latest_file, creds)

    now = np_datetime.now()
    previous_month = get_month_name_np(now.month - 1)
    options = [
        MenuOption(
            f"Get {previous_month} report",
            get_month_report,
            kwargs={"year": now.year, "month": now.month - 1},
        ),
        MenuOption(
            "Get report for another month",
            get_report_for_another_month,
        ),
        MenuOption(
            "Select custom date range",
            select_custom_date_range,
        )
    ]

    menu = Menu("Report Generator", options)
    menu.run()
