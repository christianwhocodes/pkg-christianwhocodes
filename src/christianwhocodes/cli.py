from sys import argv, exit
from typing import NoReturn

from .helpers import ExitCode, generate_random_string, version_placeholder
from .stdout import print


def main() -> NoReturn:
    match argv[1]:
        case "v" | "-v" | "--ver" | "--version" | "version":
            try:
                from importlib.metadata import version

                print(version("christianwhocodes"))
            except Exception as e:
                print(
                    version_placeholder() + ": Could not determine version\n" + str(e)
                )
                exit(ExitCode.ERROR)

        case "generaterandom" | "random" | "randomstring":
            generate_random_string()

        case _:
            print(
                "...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32"
            )

    exit(ExitCode.SUCCESS)


if __name__ == "__main__":
    main()
