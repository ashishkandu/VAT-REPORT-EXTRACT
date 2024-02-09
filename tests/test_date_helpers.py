import random

from src.date_helpers import get_month_name_np

NEPALI_MONTHNAMES = ("Baishakh", "Jestha", "Asar", "Shrawan", "Bhadau", "Aswin",
                     "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra")


def test_get_month_name_np() -> None:
    """Test if returned month name is correct."""
    random_month = random.randint(1, 12)
    res_month = get_month_name_np(random_month)

    assert res_month == NEPALI_MONTHNAMES[random_month - 1]
