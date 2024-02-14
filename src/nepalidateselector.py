from nepali_datetime import date as np_date
from nepali_datetime import _FULLMONTHNAMES as BS_MONTHS


class NepaliDateSelector:
    def __init__(self, start_year=2079):
        self.current_year = np_date.today().year
        self.allowed_years = range(start_year, self.current_year + 1)
        self.available_months = BS_MONTHS[1:]
        self.special_year = start_year

    def is_valid_year(self, year):
        return year in self.allowed_years

    def is_valid_month(self, month_index):
        return 0 <= month_index < len(self.available_months)

    def select_year(self):
        while True:
            year_str = input(
                f"\nSelect Year (from {min(self.allowed_years)} to {max(self.allowed_years)}):")
            try:
                selected_year = int(year_str)
                if not self.is_valid_year(selected_year):
                    raise ValueError(
                        f"Year must be {min(self.allowed_years)} or later!")
                return selected_year
            except ValueError:
                print("Invalid year. Please select a year within the allowed range.")

    def select_month(self, selected_year):
        # Create a local copy of self.available_months
        available_months = self.available_months

        if selected_year == self.current_year:
            available_months = available_months[:np_date.today().month]
        elif selected_year == self.special_year:  # Special check for the specified year
            # Exclude first 3 months
            available_months = available_months[3:]

        while True:
            for index, month in enumerate(available_months):
                print(f"{index+1}. {month}")
            month_str = input("\nSelect Month:")
            selected_month_index = int(month_str) - 1
            if not self.is_valid_month(selected_month_index):
                print("Invalid month selection for this year")
            else:
                selected_month = available_months[selected_month_index]
                return selected_month

    def get_year_month(self):
        selected_year = self.select_year()
        selected_month = self.select_month(selected_year)
        selected_month_index = self.available_months.index(selected_month) + 1
        return selected_year, selected_month_index
