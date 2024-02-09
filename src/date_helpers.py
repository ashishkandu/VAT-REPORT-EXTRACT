import nepali_datetime


def get_month_name_np(month: int) -> str:
    """Returns the month name as per nepali calander for the month id."""
    return nepali_datetime._FULLMONTHNAMES[month]
