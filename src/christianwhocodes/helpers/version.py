from typing import Literal

from christianwhocodes.helpers.enums import ExitCode


class Version:
    """Utility class for version-related operations."""

    @staticmethod
    def placeholder() -> Literal["X.Y.Z"]:
        """Return a version placeholder string.

        Returns:
            Literal["X.Y.Z"]: The literal placeholder version string.
        """
        return "X.Y.Z"

    @staticmethod
    def get(package: str) -> tuple[str, str]:
        """Get the package version.

        Args:
            package: Name of the package to get version for.

        Returns:
            tuple[str, str]: The package version or placeholder (if exception), and emtpy string or error message (if excpetion).
        """
        try:
            from importlib.metadata import version

            return version(package), ""
        except Exception as e:
            return (
                Version.placeholder(),
                f"Could not determine version\n{str(e)}",
            )


def print_version(package: str) -> ExitCode:
    """
    Print the package version and return appropriate exit code.

    Args:
        package: Name of the package to get version for.

    Returns:
        ExitCode.SUCCESS (0) if version found, ExitCode.ERROR otherwise
    """
    _VERSION = Version.get(package)[0]

    if _VERSION != Version.placeholder():
        print(_VERSION)
        return ExitCode.SUCCESS
    else:
        print(f"{_VERSION}: Could not determine version for package '{package}'.")
        return ExitCode.ERROR
