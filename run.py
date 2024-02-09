from typing import Callable
from nepali_datetime import datetime as np_datetime
from src.date_helpers import get_month_name_np
from src.filingmonth import FilingMonth
from src.menu import Menu, MenuOption, ReportMenu
from src.report_generator import ReportGenerator


def get_previous_month_report(**kwargs) -> None:
    """
    Retrieves the report for the previous month.

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
    # TODO: Add implementation for getting report for another month
    pass


def select_custom_date_range() -> None:
    """
    This function allows the user to select a custom date range for analysis.
    """
    # TODO: Implement the logic for selecting a custom date range
    pass


def main() -> None:  # function takes no arguments and returns nothing
    """
    Main function to handle user input and execute the selected option.
    """
    menu_options: dict[int, Callable[[], None]] = {  # dictionary with integer keys and function values
        # value is a function that takes no arguments and returns nothing
        1: get_previous_month_report,
        # value is a function that takes no arguments and returns nothing
        2: get_report_for_another_month,
        # value is a function that takes no arguments and returns nothing
        3: select_custom_date_range,
    }
    while True:
        selected_option = input("\nEnter an option from above: ")
        if selected_option.lower() in ('exit', 'break', 'no', 'n', '0'):
            # raise SystemExit with message 'Terminated'
            raise SystemExit('Terminated')
        try:
            selected_option = int(selected_option)
            menu_options[selected_option]()  # call the selected function
            break
        except (KeyError, ValueError):
            print("Please choose from above options!!")


if __name__ == "__main__":

    now = np_datetime.now()
    previous_month = get_month_name_np(now.month - 1)
    options = [
        MenuOption(
            f"Get {previous_month} report",
            get_previous_month_report,
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
