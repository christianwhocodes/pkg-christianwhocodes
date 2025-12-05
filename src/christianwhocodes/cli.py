from argparse import ArgumentParser
from sys import exit
from typing import NoReturn

from .helpers import ExitCode, Version, generate_random_string
from .stdout import print


def create_parser() -> ArgumentParser:
    """Create and configure the argument parser."""
    parser = ArgumentParser(
        prog="christianwhocodes",
        description="Christian Who Codes CLI Tool",
        epilog="...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32",
    )

    # Add version argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=Version.get("christianwhocodes")[0],
        help="Show program version",
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Random string generator subcommand
    random_parser = subparsers.add_parser(
        "random",
        aliases=["generaterandom", "randomstring"],
        help="Generate a random string",
    )
    random_parser.add_argument(
        "--no-clipboard", action="store_true", help="Don't copy the result to clipboard"
    )
    random_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Length of the random string (default: 16)",
    )

    return parser


def main() -> NoReturn:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle commands using match case
    match args.command:
        case "random" | "generaterandom" | "randomstring":
            generate_random_string(length=args.length, no_clipboard=args.no_clipboard)
        case _:
            print(
                "...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32"
            )

    exit(ExitCode.SUCCESS)


if __name__ == "__main__":
    main()
