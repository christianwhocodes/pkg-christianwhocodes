from abc import ABC, abstractmethod
from enum import StrEnum
from os import environ
from pathlib import Path
from platform import system
from stat import S_IRUSR, S_IWUSR

from christianwhocodes.helpers.stdout import Text, print


class FileGenerator(ABC):
    """Abstract base class for generating configuration files.

    Subclasses must implement `file_path` and `data` properties to define
    where the file should be created and what content it should contain.
    """

    @property
    @abstractmethod
    def file_path(self) -> Path:
        """Default file path. Subclasses must override."""
        ...

    @property
    @abstractmethod
    def data(self) -> str:
        """Default file content. Subclasses must override."""
        ...

    def _confirm_overwrite_if_file_exists(self, force: bool = False) -> bool:
        """Check if the file has content and ask to overwrite.

        Args:
            force: If True, skip confirmation and allow overwrite.

        Returns:
            bool: True if file should be written, False if operation should be aborted.
        """
        if (
            self.file_path.exists()
            and self.file_path.is_file()
            and self.file_path.stat().st_size > 0
            and not force
        ):
            attempts = 0
            while attempts < 3:
                print(f"'{self.file_path}' exists and is not empty", Text.WARNING)
                resp = input("overwrite? [y/N]: ").strip().lower()
                match resp:
                    case "y" | "yes":
                        return True
                    case "n" | "no" | "":
                        print("Aborted.", Text.WARNING)
                        return False
                    case _:
                        print("Please answer with 'y' or 'n'.", Text.INFO)
                        attempts += 1
            print("Too many invalid responses. Aborted.", Text.WARNING)
            return False
        else:
            return True

    def create(self, force: bool = False) -> None:
        """Create or overwrite the file with overridable path and data.

        Args:
            force: If True, overwrite without confirmation.
        """
        if not self._confirm_overwrite_if_file_exists(force):
            return  # Abort

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write data provided by subclass
        self.file_path.write_text(self.data)
        print(f"File written to {self.file_path}", Text.SUCCESS)


class FileGeneratorOption(StrEnum):
    """Available file generator options for configuration files.

    Attributes:
        PG_SERVICE: PostgreSQL service configuration file (.pg_service.conf).
        PGPASS: PostgreSQL password file (pgpass.conf or .pgpass).
        SSH_CONFIG: SSH configuration file (~/.ssh/config).
    """

    PG_SERVICE = "pg_service"
    PGPASS = "pgpass"
    SSH_CONFIG = "ssh_config"


class PgServiceFileGenerator(FileGenerator):
    """Generator for PostgreSQL service configuration file (.pg_service.conf).

    Creates a pg_service.conf file in the appropriate location based on the OS:
    - Windows: %APPDATA%/postgresql/.pg_service.conf
    - Unix/Linux/macOS: ~/.pg_service.conf
    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the pg_service.conf file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / ".pg_service.conf"
            case _:
                return Path("~/.pg_service.conf").expanduser()

    @property
    def data(self) -> str:
        """Return template content for pg_service.conf file."""
        return (
            "# Read more about pg_service file: https://www.postgresql.org/docs/current/libpq-pgservice.html\n\n"
            "# comment\n"
            "[mydb]\n"
            "host=localhost\n"
            "port=5432\n"
            "dbname=postgres\n"
            "user=postgres\n"
        )


class PgPassFileGenerator(FileGenerator):
    """Generator for PostgreSQL password file (pgpass.conf or .pgpass).

    Creates a pgpass file in the appropriate location based on the OS:
    - Windows: %APPDATA%/postgresql/pgpass.conf
    - Unix/Linux/macOS: ~/.pgpass

    On Unix-like systems, sets file permissions to 600 for security.
    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the pgpass file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / "pgpass.conf"
            case _:
                return Path("~/.pgpass").expanduser()

    @property
    def data(self) -> str:
        """Return template content for pgpass file."""
        return (
            "# Read more about pgpass file: https://www.postgresql.org/docs/current/libpq-pgpass.html\n\n"
            "# This file should contain lines of the following format:\n"
            "# hostname:port:database:username:password\n"
        )

    def create(self, force: bool = False) -> None:
        """Create or overwrite pgpass file with strict permissions.

        Args:
            force: If True, overwrite without confirmation.

        Note:
            On Unix-like systems, this method sets file permissions to 600 (owner read/write only)
            as required by PostgreSQL for security.
        """
        super().create(force=force)

        if system() != "Windows":
            try:
                self.file_path.chmod(S_IRUSR | S_IWUSR)  # chmod 600
                print(f"Permissions set to 600 for {self.file_path}", Text.SUCCESS)
            except Exception as e:
                print(
                    f"Warning: could not set permissions on {self.file_path}: {e}",
                    Text.WARNING,
                )


class SSHConfigFileGenerator(FileGenerator):
    """Generator for SSH configuration file (~/.ssh/config).

    Creates an SSH config file with a template host configuration.
    """

    @property
    def file_path(self) -> Path:
        """Return the path for the SSH config file (~/.ssh/config)."""
        return Path("~/.ssh/config").expanduser()

    @property
    def data(self) -> str:
        """Return template content for SSH config file."""
        return (
            "# Read more about SSH config files: https://linux.die.net/man/5/ssh_config\n"
            "# ssh -i 'path/to/key' user@domain_or_ip\n\n"
            "Host my_host_alias\n"
            "    IdentityFile D:/.ssh/key\n"
            "    User my_user\n"
            "    HostName my_domain_or_ip_address\n"
            "#    LocalForward 8080 localhost:8080\n"
        )
