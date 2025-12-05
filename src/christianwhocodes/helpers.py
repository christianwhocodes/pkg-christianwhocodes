from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from tomllib import load as load_toml
from typing import Any, Callable, Iterable, Literal, cast


def version_placeholder() -> Literal["X.Y.Z"]:
    """Return a version placeholder string.

    Returns:
        Literal["X.Y.Z"]: The literal placeholder version string.
    """
    return "X.Y.Z"


# ======================================================================
# PYPROJECT PARSING
# ======================================================================


class PyProject:
    """Represents the whole data of a pyproject.toml file.

    Attributes:
        path (Path): The path to the pyproject.toml file.
        data (dict[str, Any]): Parsed data from the `[project]` section.

    Example:
        >>> py = PyProject(Path("pyproject.toml"))
        >>> py.name
        'my-package'
        >>> py.version
        '1.0.0'
        >>> urls = py.data.get("project", {}).get("urls", {})
        >>> urls.repository
        'https://github.com/org/repo'
    """

    def __init__(self, toml_path: Path) -> None:
        """Load and parse the pyproject file.

        Args:
            toml_path: Path to the pyproject.toml file.

        Raises:
            FileNotFoundError: If the file does not exist.
            tomllib.TOMLDecodeError: If the file is invalid TOML.
            KeyError: If the `[project]` section is missing.
        """
        self._toml_path = toml_path

        with open(toml_path, "rb") as f:
            full_data = load_toml(f)

        if "project" not in full_data:
            raise KeyError(f"[project] section not found in {toml_path}")
        else:
            self._data: dict[str, Any] = full_data

    # ----------------------------
    # Metadata Properties
    # ----------------------------

    @property
    def name(self) -> str:
        """Return the project name.

        Raises:
            KeyError: If missing.
        """
        return self._data["project"]["name"]

    @property
    def version(self) -> str:
        """Return the project version.

        Raises:
            KeyError: If missing.
        """
        return self._data["project"]["version"]

    @property
    def description(self) -> str | None:
        """Return the project description, if any."""
        return self._data["project"].get("description")

    @property
    def authors(self) -> list[dict[str, str]]:
        """Return a list of project authors."""
        return self._data["project"].get("authors", [])

    @property
    def dependencies(self) -> list[str]:
        """Return project dependencies."""
        return self._data["project"].get("dependencies", [])

    @property
    def python_requires(self) -> str | None:
        """Return the required Python version."""
        return self._data["project"].get("requires-python")

    # ----------------------------
    # General Accessors
    # ----------------------------

    @property
    def data(self) -> dict[str, Any]:
        """Return raw metadata."""
        return self._data

    @property
    def path(self) -> Path:
        """Return the pyproject.toml file path."""
        return self._toml_path


class PyProjectSection:
    """Represents an arbitrary section inside a pyproject.toml file.

    Allows loading nested dot-notation sections such as:

        PyProjectSection("tool.tawala", path)

    Example:
        >>> sec = PyProjectSection("tool.poetry", Path("pyproject.toml"))
        >>> sec.data
        {'name': 'mypkg', 'dependencies': {...}}

    Args:
        section (str): Dot-separated section path.
        toml_path (Path): Path to the pyproject.toml file.
    """

    def __init__(self, section: str, toml_path: Path) -> None:
        self._section = section
        self._toml_path = toml_path

        with open(toml_path, "rb") as f:
            data = load_toml(f)

        current = data
        for key in section.split("."):
            if not isinstance(current, dict) or key not in current:
                raise KeyError(f"Section '{section}' not found in {toml_path}")
            current = current[key]

        self._data: dict[str, Any] = current

    @property
    def section(self) -> str:
        """Return the dot-path of this section."""
        return self._section

    @property
    def path(self) -> Path:
        """Return the file path."""
        return self._toml_path

    @property
    def data(self) -> dict[str, Any]:
        """Return the section data."""
        return self._data


# ======================================================================
# UTILITY FUNCTIONS
# ======================================================================


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Return the maximum string length among a list of `(value, display)` pairs.

    Args:
        choices: Iterable of (value, display) tuples.

    Returns:
        int: The maximum length of the value field.
    """
    return max(len(choice[0]) for choice in choices)


# ======================================================================
# EXIT CODES
# ======================================================================


class ExitCode(IntEnum):
    """Standard exit codes.

    SUCCESS = 0
    ERROR = 1
    """

    SUCCESS = 0
    ERROR = 1


# ======================================================================
# TYPE CONVERSIONS
# ======================================================================


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
