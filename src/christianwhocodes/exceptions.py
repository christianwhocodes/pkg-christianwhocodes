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
            message = (
                "Not running in expected " + f"{self.expected_dir} "
                if self.expected_dir
                else "" + f"directory! Current directory: {self.current_dir}"
            )

        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format the error message with directory information."""
        parts = [
            f"DirectoryError: {self.message}",
            f"Expected Directory: {self.expected_dir}",
            f"Current Directory: {self.current_dir}",
        ]

        if self.color:
            try:
                from io import StringIO
                from sys import stdout

                from .stdout import Text, print

                # Capture colored output to string
                output = StringIO()
                old_stdout = stdout
                stdout = output

                print([("DirectoryError: ", Text.ERROR), (self.message, None)])
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
            except ImportError:
                # Fall back to plain text if colors module not available
                pass

        return "\n".join(parts)
