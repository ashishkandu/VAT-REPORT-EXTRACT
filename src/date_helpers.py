import nepali_datetime


def get_month_name_np(month: int) -> str:
    """Returns the month name as per Nepali calendar for the given month ID.

    Args:
        month (int): The month as number(1-12).

    Returns:
        str: The month name.
    """
    return nepali_datetime._FULLMONTHNAMES[month]
