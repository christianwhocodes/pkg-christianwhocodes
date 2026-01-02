from pathlib import Path
from tomllib import load
from typing import Any


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
            full_data = load(f)

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
