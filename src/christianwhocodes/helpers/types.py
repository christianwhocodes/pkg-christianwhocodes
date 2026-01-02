import os
from pathlib import Path
from typing import Any, Callable, cast


class TypeConverter:
    """Utility class for converting basic data types."""

    @staticmethod
    def to_bool(value: str | bool) -> bool:
        """Convert a string or boolean to a boolean.

        Truthy strings:
            'true', '1', 'yes', 'on'
        """
        if isinstance(value, bool):
            return value
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def to_list_of_str(
        value: Any, transform: Callable[[str], str] | None = None
    ) -> list[str]:
        """Convert a string or list into a list of strings.

        Args:
            value: List or comma-separated string.
            transform: Optional string transformer (e.g. str.lower).

        Returns:
            list[str]: Cleaned list of strings.
        """
        result: list[str] = []

        if isinstance(value, list):
            list_value = cast(list[Any], value)
            result = [str(item) for item in list_value]

        elif isinstance(value, str):
            result = [item.strip() for item in value.split(",") if item.strip()]

        if transform:
            result = [transform(item) for item in result]

        return result

    @staticmethod
    def to_path(value: str | Path, resolve: bool = True) -> Path:
        """Convert a string or Path to a properly expanded and resolved Path.

        This method intelligently handles:
        - User home directory expansion (~)
        - Environment variable expansion ($VAR, ${VAR})
        - Absolute path resolution
        - Relative path resolution (optional)

        Args:
            value: String path or Path object to convert.
            resolve: If True, resolve to absolute path (default: True).

        Returns:
            Path: Processed Path object.

        Examples:
            >>> TypeConverter.to_path("~/documents/file.txt")
            PosixPath('/home/user/documents/file.txt')
            >>> TypeConverter.to_path("$HOME/file.txt")
            PosixPath('/home/user/file.txt')
            >>> TypeConverter.to_path("./relative/path", resolve=False)
            PosixPath('relative/path')
        """
        # Convert to Path if string
        if isinstance(value, str):
            path = Path(value)
        else:
            path = value

        # Expand user home directory (~)
        if "~" in str(path):
            path = path.expanduser()

        # Expand environment variables
        path_str = str(path)
        if "$" in path_str:
            path = Path(os.path.expandvars(path_str))

        # Resolve to absolute path if requested
        if resolve:
            path = path.resolve()

        return path
