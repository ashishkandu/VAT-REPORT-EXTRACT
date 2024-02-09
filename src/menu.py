from nepali_datetime import datetime as datetime_np
from typing import List

from src.books import Book, Books


class MenuOption:
    """
    A menu option.
    """

    def __init__(self, name: str, function: callable, args=None, kwargs=None):
        """
        Initializes a new instance of the class with the given name, function, args, and kwargs.

        :param name: str - the name of the option
        :param function: callable - the function to be associated with the option
        :param args: list - optional arguments for the function (default [])
        :param kwargs: dict - optional keyword arguments for the function (default {})
        """
        self.name = name
        self.function = function
        self.args = args or []
        self.kwargs = kwargs or {}

    def execute(self):
        """
        Executes the function with the provided arguments and keyword arguments.
        """
        self.function(*self.args, **self.kwargs)


class Menu:
    """
    A menu class.
    """

    def __init__(self, title: str, options: List[MenuOption]):
        """
        Initializes the class with the given title and options.

        Args:
            title (str): The title of the menu.
            options (List[MenuOption]): The list of menu options.

        Returns:
            None
        """
        self.title = title
        self.options = options

    def display_welcome_message(self) -> None:
        """
        Display a welcome message along with the current date and time, and print the title and options.
        """
        now = datetime_np.now()
        print(f"Hi there, [{now.strftime('%d %B, %Y %I:%M %p')}]")
        print(f"\n### {self.title} ###\n")
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option.name}")

    def prompt_user(self) -> int:
        """
        Prompt the user to enter an option from a list, validate the input, and return the selected option index.
        Returns:
            int: The index of the selected option.
        """
        try:
            selected_option = int(input("Enter an option from above: "))
            if selected_option < 1 or selected_option > len(self.options):
                raise ValueError("Invalid option selected.")
            return selected_option - 1
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return self.prompt_user()

    def run(self) -> None:
        """
        A method that runs the program, displays a welcome message, prompts the user for input, executes the selected option, and allows the user to exit the program.
        """
        self.display_welcome_message()
        while True:
            selected_option = self.prompt_user()
            self.options[selected_option].execute()
            if input("Do you want to exit? (y/n): ").lower() == "y":
                break


class ReportMenu:
    """
    A class for the report menu, which displays a list of books and allows the user to select one.
    """

    def __init__(self, books: List[Book] = Books.list()):
        """
        Initializes the class instance with a list of books.

        :param books: A list of Book objects. Defaults to the list of all books.
        :type books: List[Book]
        """
        self.books = books[:-1]

    def display_menu(self) -> None:
        """
        Display the report selection menu, listing the available books and an option for all reports.
        """
        print("\n### Report Selection Menu ###\n")
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book.name.title()}")
        print("3. All reports")

    def prompt_user_for_book(self) -> Book:
        """
        Prompt the user for a book selection and return the selected book.
        If the user selects option 3, return None to indicate all books.
        """
        while True:
            self.display_menu()
            try:
                selection = int(input("Enter your selection (1-3): "))
                if 1 <= selection <= 3:
                    if selection == 3:
                        return None  # All books
                    else:
                        return self.books[selection - 1]
                else:
                    raise ValueError
            except ValueError:
                print("Invalid selection. Please enter a number between 1 and 3.")
