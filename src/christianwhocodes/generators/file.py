from abc import ABC, abstractmethod
from os import environ
from pathlib import Path
from platform import system
from stat import S_IRUSR, S_IWUSR

from ..stdout import Text, print


class FileGenerator(ABC):
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
        """Check if the file has content and ask to overwrite."""
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
        """Create or overwrite the file with overridable path and data."""
        if not self._confirm_overwrite_if_file_exists(force):
            return  # Abort

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write data provided by subclass
        self.file_path.write_text(self.data)
        print(f"File written to {self.file_path}", Text.SUCCESS)


class PgServiceFileGenerator(FileGenerator):
    @property
    def file_path(self) -> Path:
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / ".pg_service.conf"
            case _:
                return Path("~/.pg_service.conf").expanduser()

    @property
    def data(self) -> str:
        return (
            "# https://www.postgresql.org/docs/current/libpq-pgservice.html\n\n"
            "# comment\n"
            "[mydb]\n"
            "host=localhost\n"
            "port=5432\n"
            "dbname=postgres\n"
            "user=postgres\n"
        )


class PgPassFileGenerator(FileGenerator):
    @property
    def file_path(self) -> Path:
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / "pgpass.conf"
            case _:
                return Path("~/.pgpass").expanduser()

    @property
    def data(self) -> str:
        return (
            "# https://www.postgresql.org/docs/current/libpq-pgpass.html\n\n"
            "# This file should contain lines of the following format:\n"
            "# hostname:port:database:username:password\n"
        )

    def create(self, force: bool = False) -> None:
        """Create or overwrite pgpass file with strict permissions."""
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
