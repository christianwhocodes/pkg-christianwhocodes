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
                import sys
                from io import StringIO

                from christianwhocodes.colors import Text, colored_print

                # Capture colored output to string
                output = StringIO()
                old_stdout = sys.stdout
                sys.stdout = output

                colored_print([("DirectoryError: ", Text.ERROR), (self.message, None)])
                colored_print(
                    [
                        ("Expected Directory: ", Text.INFO),
                        (str(self.expected_dir), Text.HIGHLIGHT),
                    ]
                )
                colored_print(
                    [
                        ("Current Directory: ", Text.WARNING),
                        (str(self.current_dir), Text.HIGHLIGHT),
                    ]
                )

                sys.stdout = old_stdout
                return output.getvalue().rstrip()
            except ImportError:
                # Fall back to plain text if colors module not available
                pass

        return "\n".join(parts)


# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage with expected directory (colored by default)
    def example_1() -> None:
        print("Example 1: Basic usage with expected directory (colored by default)")
        try:
            raise DirectoryNotFoundError(expected_dir="project_root")
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 2: Custom message with expected directory
    def example_2() -> None:
        print("Example 2: Custom message with expected directory")
        try:
            raise DirectoryNotFoundError(
                message="Cannot find configuration files", expected_dir="config"
            )
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 3: With custom current directory
    def example_3() -> None:
        print("Example 3: With custom current directory")
        try:
            raise DirectoryNotFoundError(
                expected_dir="app", current_dir="/home/user/wrong_location"
            )
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 4: Minimal usage (no parameters)
    def example_4() -> None:
        print("Example 4: Minimal usage (no parameters)")
        try:
            raise DirectoryNotFoundError()
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 5: Practical use case - checking for project directory
    def example_5() -> None:
        print("Example 5: Practical use case - checking for project directory")

        def check_project_directory():
            """Check if running in a valid project directory."""
            current = Path.cwd()
            # Check for common project markers
            if (
                not (current / "pyproject.toml").exists()
                and not (current / "setup.py").exists()
            ):
                raise DirectoryNotFoundError(
                    message="Project configuration files not found",
                    expected_dir="Python Project Root",
                    current_dir=str(current),
                )
            print(f"✓ Running in valid project directory: {current}")

        try:
            check_project_directory()
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 6: Accessing exception attributes
    def example_6() -> None:
        print("Example 6: Accessing exception attributes")
        try:
            raise DirectoryNotFoundError(
                expected_dir="Data", current_dir="/tmp/wrong_path"
            )
        except DirectoryNotFoundError as e:
            print(f"Message: {e.message}")
            print(f"Expected: {e.expected_dir}")
            print(f"Current: {e.current_dir}")
        print()

    # Example 7: Disabling colored output
    def example_7() -> None:
        print("Example 7: Disabling colored output explicitly")
        try:
            raise DirectoryNotFoundError(
                message="Configuration directory missing",
                expected_dir="config",
                current_dir="/home/user/project",
                color=False,
            )
        except DirectoryNotFoundError as e:
            print(e)
        print()

    # Example 8: Colored output in practical use (default behavior)
    def example_8() -> None:
        print("Example 8: Colored output in practical validation (default)")

        def check_data_directory(use_color: bool = True):
            """Check if data directory exists."""
            data_dir = Path.cwd() / "data"
            if not data_dir.exists():
                raise DirectoryNotFoundError(
                    message="Data directory not found",
                    expected_dir="data",
                    current_dir=str(Path.cwd()),
                    color=use_color,
                )

        try:
            check_data_directory()
        except DirectoryNotFoundError as e:
            print(e)

    # See the examples one by one or call them all at once
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
    example_6()
    example_7()
    example_8()
