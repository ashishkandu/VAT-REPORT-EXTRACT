from unittest.mock import Mock
from src.books import Book
from src.menu import Menu, MenuOption, ReportMenu


class TestMenuOption:
    def test_menu_option_initialization(self):
        """
        Test the initialization of MenuOption with required and default parameters.
        """
        # Test initialization with required parameters
        option = MenuOption("Option 1", lambda x: x, [1], {"key": "value"})
        assert option.name == "Option 1"
        assert option.function(2) == 2
        assert option.args == [1]
        assert option.kwargs == {"key": "value"}

        # Test initialization with default args and kwargs
        option = MenuOption("Option 2", lambda x: x)
        assert option.name == "Option 2"
        assert option.function(2) == 2
        assert option.args == []
        assert option.kwargs == {}

    def test_menu_option_execution(self):
        """
        Test the execution of MenuOption objects.
        """

        # Test execution with arguments and keyword arguments
        option = MenuOption("Option 3", lambda x, y: x + y, [3], {"y": 4})
        assert option.execute() == 7

        # Test execution without arguments and keyword arguments
        option = MenuOption("Option 4", lambda: "hello")
        assert option.execute() == "hello"


class TestMenu:
    def setup_method(self):
        """
        Set up the method by initializing options with MenuOption objects and creating a Menu with the options.
        """
        self.options = [MenuOption("Option 1", lambda: print(
            "Option 1 selected")), MenuOption("Option 2", lambda: print("Option 2 selected"))]
        self.menu = Menu("Test Menu", self.options)

    def test_menu_initialization(self):
        """
        Test the initialization of the menu, checking the title and options.
        """
        assert self.menu.title == "Test Menu"
        assert self.menu.options == self.options

    def test_display_welcome_message(self, capsys):
        """
        Function to test the display of a welcome message.

        Args:
            self: the instance of the class
            capsys: the capturing system for stdout and stderr

        Returns:
            None
        """
        self.menu.display_welcome_message()
        captured = capsys.readouterr()
        assert "Test Menu" in captured.out

    def test_prompt_user(self, monkeypatch):
        """
        Function to test the prompt_user method by mocking user input.
        Parameters:
        - self: the instance of the class
        - monkeypatch: the pytest monkeypatch fixture
        """
        monkeypatch.setattr('builtins.input', lambda _: "1")
        assert self.menu.prompt_user() == 0

    def test_run(self, monkeypatch, capsys):
        """
        Function to test the run method with simulated user input using monkeypatch and capsys.
        """

        # Simulate user input of "1" followed by "y"
        input_values = iter(["1", "y"])
        monkeypatch.setattr('builtins.input', lambda _: next(input_values))

        self.menu.run()
        captured = capsys.readouterr()
        assert "Hi there" in captured.out
        assert "1. Option 1" in captured.out
        assert "2. Option 2" in captured.out


class TestReportMenu:
    def setup_method(self):
        """
        Setup method for initializing test data for the test case.
        """
        book1 = Mock(spec=Book)
        book1.name = "book1"
        book2 = Mock(spec=Book)
        book2.name = "book2"
        temp_book = Mock(spec=Book)
        self.books = [book1, book2, temp_book]

    def test_display_menu(self, capsys):
        """
        Function to test the display menu functionality.

        Args:
            self: The instance of the class.
            capsys: The built-in pytest fixture to capture stdout and stderr.

        Returns:
            None
        """
        report_menu = ReportMenu(self.books)
        report_menu.display_menu()
        captured = capsys.readouterr()
        assert "1. Book1" in captured.out
        assert "2. Book2" in captured.out
        assert "3. All reports" in captured.out

    def test_prompt_user_for_book_all_books(self, monkeypatch):
        """
        Test prompt_user_for_book method with all books.

        Args:
        - self: the TestClass instance
        - monkeypatch: pytest monkeypatch fixture

        Returns:
        - None
        """
        # Create a ReportMenu instance with all books
        report_menu = ReportMenu(self.books)

        # Patch the builtins.input function to return "3"
        monkeypatch.setattr('builtins.input', lambda _: "3")

        # Call prompt_user_for_book and assert selected_book is None
        selected_book = report_menu.prompt_user_for_book()
        assert selected_book is None

    def test_prompt_user_for_book_selected_book(self, monkeypatch):
        """
        Test prompt_user_for_book method in ReportMenu class.
        """
        # Arrange
        report_menu = ReportMenu(self.books)
        user_input = "1"

        # Act
        monkeypatch.setattr('builtins.input', lambda _: user_input)
        selected_book = report_menu.prompt_user_for_book()

        # Assert
        assert selected_book.name == "book1"

    def test_prompt_user_for_book_invalid_selection(self, monkeypatch, capsys):
        """
        Test the prompt_user_for_book method with an invalid book selection.
        """
        report_menu = ReportMenu(self.books)
        user_input = iter(["999", "2"])
        monkeypatch.setattr('builtins.input', lambda _: next(user_input))
        selected_book = report_menu.prompt_user_for_book()
        captured = capsys.readouterr()
        assert "Invalid selection" in captured.out
        assert selected_book.name == "book2"
