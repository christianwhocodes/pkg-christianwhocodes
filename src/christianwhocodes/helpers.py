from enum import IntEnum
from pathlib import Path
from tomllib import load as load_toml
from typing import Any, Callable, Iterable, Literal, cast


def version_placeholder() -> Literal["X.Y.Z"]:
    """Return a version placeholder string.

    Returns:
        str: The literal string "X.Y.Z" used as a placeholder for version numbers.
    """
    return "X.Y.Z"


class PyProject:
    """Parser for pyproject.toml files.

    Provides convenient access to common fields in a pyproject.toml file,
    such as project name, version, description, and other metadata.

    Args:
        toml_path: Path to the pyproject.toml file.

    Raises:
        FileNotFoundError: If the specified toml file does not exist.
        tomllib.TOMLDecodeError: If the file is not valid TOML format.

    Example:
        >>> from pathlib import Path
        >>> pyproject = PyProject(Path("pyproject.toml"))
        >>> pyproject.name
        'my-package'
        >>> pyproject.version
        '1.0.0'
    """

    def __init__(self, toml_path: Path) -> None:
        """Initialize the PyProject instance by reading the toml file.

        Args:
            toml_path: Path to the pyproject.toml file.
        """
        self._toml_path = toml_path
        with open(toml_path, "rb") as f:
            self._data = load_toml(f)

    @property
    def name(self) -> str:
        """Get the project name.

        Returns:
            str: The project name from the [project] section.

        Raises:
            KeyError: If the name field is missing.
        """
        return self._data["project"]["name"]

    @property
    def version(self) -> str:
        """Get the project version.

        Returns:
            str: The project version from the [project] section.

        Raises:
            KeyError: If the version field is missing.
        """
        return self._data["project"]["version"]

    @property
    def description(self) -> str | None:
        """Get the project description.

        Returns:
            str | None: The project description, or None if not specified.
        """
        return self._data.get("project", {}).get("description")

    @property
    def authors(self) -> list[dict[str, str]]:
        """Get the list of project authors.

        Returns:
            list[dict[str, str]]: List of author dictionaries with 'name' and
                optionally 'email' keys. Returns empty list if not specified.
        """
        return self._data.get("project", {}).get("authors", [])

    @property
    def dependencies(self) -> list[str]:
        """Get the project dependencies.

        Returns:
            list[str]: List of dependency specifications. Returns empty list
                if not specified.
        """
        return self._data.get("project", {}).get("dependencies", [])

    @property
    def python_requires(self) -> str | None:
        """Get the Python version requirement.

        Returns:
            str | None: The Python version requirement string, or None if not specified.
        """
        return self._data.get("project", {}).get("requires-python")

    @property
    def data(self) -> dict[str, Any]:
        """Get the raw parsed TOML data.

        Returns:
            dict[str, Any]: The complete parsed pyproject.toml data.
        """
        return self._data

    @property
    def path(self) -> Path:
        """Get the path to the pyproject.toml file.

        Returns:
            Path: The path to the pyproject.toml file.
        """
        return self._toml_path


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Get the maximum length of choice values.

    Args:
        choices: An iterable of (value, display) tuples where the first element
            is the choice value whose length will be measured.

    Returns:
        int: The length of the longest choice value in the iterable.

    Example:
        >>> choices = [("short", "Short"), ("medium_size", "Medium"), ("x", "X")]
        >>> max_length_from_choices(choices)
        11
    """
    return max(len(choice[0]) for choice in choices)


class ExitCode(IntEnum):
    """Standard exit codes for program termination.

    Used to indicate whether a program completed successfully or encountered an error.
    Follows Unix convention where 0 indicates success and non-zero indicates failure.

    Example:
        >>> from sys import exit

        >>> from christianwhocodes.helpers import ExitCode

        >>> def main() -> ExitCode:
        ...     try:
        ...         # Do some work
        ...     except Exception:
        ...         return ExitCode.ERROR    # Exit with code 1
        ...     else:
        ...         return ExitCode.SUCCESS  # Exit with code 0

        >>> if __name__ == "__main__":
        ...     exit(main())
    """

    SUCCESS = 0
    ERROR = 1


class TypeConverter:
    """Utility class for converting values between different types.

    Provides static methods for common type conversions such as converting
    strings to booleans or parsing comma-separated values into lists.

    Example:
        >>> TypeConverter.to_bool("yes")
        True
        >>> TypeConverter.to_list_of_str("a,b,c")
        ['a', 'b', 'c']
    """

    @staticmethod
    def to_bool(value: str | bool) -> bool:
        """Convert a string or boolean value to a boolean.

        Accepts boolean values as-is and converts string representations
        of truthy values ('true', '1', 'yes', 'on') to True. All other
        strings are converted to False. String comparison is case-insensitive.

        Args:
            value: A boolean value or string to be converted.

        Returns:
            bool: The converted boolean value.

        Example:
            >>> TypeConverter.to_bool(True)
            True
            >>> TypeConverter.to_bool("yes")
            True
            >>> TypeConverter.to_bool("TRUE")
            True
            >>> TypeConverter.to_bool("no")
            False
        """
        if isinstance(value, bool):
            return value
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def to_list_of_str(
        value: Any, transform: Callable[[str], str] | None = None
    ) -> list[str]:
        """Convert a value to a list of strings with optional transformation.

        Handles conversion from lists (converting each element to string) and
        comma-separated strings (splitting and stripping whitespace). Empty
        strings after stripping are excluded from the result.

        Args:
            value: The value to convert. Can be a list or a comma-separated string.
            transform: Optional function to apply to each string element
                (e.g., str.lower, str.upper, str.strip).

        Returns:
            list[str]: The converted and optionally transformed list of strings.

        Example:
            >>> TypeConverter.to_list_of_str("a, b, c")
            ['a', 'b', 'c']
            >>> TypeConverter.to_list_of_str("Apple,Banana", transform=str.lower)
            ['apple', 'banana']
            >>> TypeConverter.to_list_of_str([1, 2, 3])
            ['1', '2', '3']
            >>> TypeConverter.to_list_of_str("a,  , b")
            ['a', 'b']
        """
        result: list[str] = []

        if isinstance(value, list):
            # Cast to list[Any] to help type checker understand iteration
            list_value = cast(list[Any], value)
            result = [str(item) for item in list_value]
        elif isinstance(value, str):
            result = [item.strip() for item in value.split(",") if item.strip()]

        if transform:
            result = [transform(item) for item in result]

        return result
