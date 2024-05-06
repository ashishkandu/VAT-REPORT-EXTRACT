import nepali_datetime


def get_month_name_np(month: int) -> str:
    """Returns the month name as per Nepali calendar for the given month ID.

    Args:
        month (int): The month as number(1-12).

    Returns:
        str: The month name.
    """
    return nepali_datetime._FULLMONTHNAMES[month]


def get_previous_month_and_year(current_month: int, current_year: int) -> tuple[int, int]:
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year
    return previous_month, previous_year