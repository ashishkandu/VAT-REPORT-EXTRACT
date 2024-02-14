from nepali_datetime import date as np_date
from nepali_datetime import _FULLMONTHNAMES as BS_MONTHS


class NepaliDateSelector:
    def __init__(self, start_year=2079):
        self.current_year = np_date.today().year
        self.allowed_years = range(start_year, self.current_year + 1)
        self.available_months = BS_MONTHS[1:]

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
        if selected_year == self.current_year:
            self.available_months = self.available_months[:np_date.today(
            ).month]
        elif selected_year == 2079:  # Special check for 2079
            # Exclude first 3 months
            self.available_months = self.available_months[3:]

        while True:
            for index, month in enumerate(self.available_months):
                print(f"{index+1}. {month}")
            month_str = input("\nSelect Month:")
            try:
                selected_month_index = int(month_str) - 1
                if not self.is_valid_month(selected_month_index):
                    raise ValueError("Invalid month selection for this year")

                selected_month = self.available_months[selected_month_index]
                return selected_month
            except ValueError:
                print("Invalid month. Please select a valid month.")

    def get_year_month(self):
        selected_year = self.select_year()
        selected_month = self.select_month(selected_year)
        selected_month_index = BS_MONTHS[:].index(selected_month)
        return selected_year, selected_month_index
