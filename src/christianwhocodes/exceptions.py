from pathlib import Path


class DirectoryNotFoundError(Exception):
    """
    Exception raised when code is not running in the expected directory.

    Attributes:
        message: Custom error message (optional, has default)
        expected_dir: The name/type of the expected directory (e.g., 'Base', 'App', 'Public')
        current_dir: The actual current working directory
        color: Whether to use colored output (requires colors module, defaults to True)
    """

    def __init__(
        self,
        message: str | None = None,
        expected_dir: str | None = None,
        current_dir: str | None = None,
        color: bool = True,
    ):
        self.expected_dir = expected_dir
        self.current_dir = current_dir or Path.cwd()
        self.color = color

        # Default message if none provided
        if message is None:
            expected_part = f"{self.expected_dir} " if self.expected_dir else ""
            message = f"Not running in expected {expected_part}directory! Current directory: {self.current_dir}"

        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format the error message with directory information."""

        if self.color:
            from io import StringIO
            from sys import stdout

            from .stdout import Text, print

            # Capture colored output to string
            output = StringIO()
            old_stdout = stdout
            stdout = output

            print([("Directory Error: ", Text.ERROR), (self.message, None)])

            # Only print expected directory if provided
            if self.expected_dir:
                print(
                    [
                        ("Expected Directory: ", Text.INFO),
                        (str(self.expected_dir), Text.HIGHLIGHT),
                    ]
                )

            print(
                [
                    ("Current Directory: ", Text.WARNING),
                    (str(self.current_dir), Text.HIGHLIGHT),
                ]
            )

            stdout = old_stdout
            return output.getvalue().rstrip()
        else:
            parts = [f"Directory Error: {self.message}"]

            # Only include expected directory if it was provided
            if self.expected_dir:
                parts.append(f"Expected Directory: {self.expected_dir}")

            parts.append(f"Current Directory: {self.current_dir}")
            return "\n".join(parts)


class IdentifierNotFoundError(Exception):
    """
    Exception raised when an identifier is not found or doesn't match expectations.

    Attributes:
        message: Custom error message (optional, has default)
        expected_identifier: The expected identifier (optional)
        color: Whether to use colored output (requires colors module, defaults to True)
    """

    def __init__(
        self,
        message: str | None = None,
        expected_identifier: str | None = None,
        color: bool = True,
    ):
        self.expected_identifier = expected_identifier
        self.color = color

        # Default message if none provided
        if message is None:
            expected_part = (
                f"{self.expected_identifier} " if self.expected_identifier else ""
            )
            message = f"Identifier {expected_part}not found!"

        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format the error message with identifier information."""

        if self.color:
            from io import StringIO
            from sys import stdout

            from .stdout import Text, print

            # Capture colored output to string
            output = StringIO()
            old_stdout = stdout
            stdout = output

            print([("Identifier Error: ", Text.ERROR), (self.message, None)])

            # Only print expected identifier if provided
            if self.expected_identifier:
                print(
                    [
                        ("Expected Identifier: ", Text.INFO),
                        (str(self.expected_identifier), Text.HIGHLIGHT),
                    ]
                )

            stdout = old_stdout
            return output.getvalue().rstrip()
        else:
            parts = [f"Identifier Error: {self.message}"]

            # Only include expected identifier if it was provided
            if self.expected_identifier:
                parts.append(f"Expected Identifier: {self.expected_identifier}")

            return "\n".join(parts)
