"""
Color definitions using the rich library.
Usage: Import these colors and use them with rich's print or Console.
"""

from enum import StrEnum

from rich.console import Console
from rich.theme import Theme as _Theme


class Theme(StrEnum):
    """Rich color codes for use in styled output."""

    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
    DEBUG = "debug"
    HIGHLIGHT = "highlight"


theme = _Theme(
    {
        Theme.ERROR: "bold red",
        Theme.WARNING: "bold yellow",
        Theme.SUCCESS: "bold green",
        Theme.INFO: "bold cyan",
        Theme.DEBUG: "bold magenta",
        Theme.HIGHLIGHT: "bold blue",
    }
)

_console = Console(theme=theme)


def colored_print(
    text: str | list[tuple[str, str | None]],
    color: str | None = None,
    end: str = "\n",
) -> None:
    """
    Print colored text using rich.

    Args:
        text: The text to print. Can be:
            - A string (used with the color parameter)
            - A list of (text, color) tuples for multi-colored output
        color: The color/style to apply (from Theme class or rich color string)
               Only used when text is a string
        end: String appended after the text (default: newline)

    Examples:
        colored_print("Error!", Theme.ERROR)
        colored_print("Status: ", Theme.INFO, end="")
        colored_print([("Error: ", Theme.ERROR), ("File not found", Theme.WARNING)])
    """
    if isinstance(text, list):
        # Multi-colored mode: text is a list of (text, color) tuples
        output = ""
        for segment_text, segment_color in text:
            if segment_color:
                output += f"[{segment_color}]{segment_text}[/{segment_color}]"
            else:
                output += segment_text
        _console.print(output, end=end)
    else:
        # Single color mode
        if color:
            _console.print(f"[{color}]{text}[/{color}]", end=end)
        else:
            _console.print(text, end=end)


# Example usage
if __name__ == "__main__":
    # Single color examples
    colored_print("This is an error message", Theme.ERROR)
    colored_print("This is a warning message", Theme.WARNING)
    colored_print("This is a success message", Theme.SUCCESS)
    colored_print("This is an info message", Theme.INFO)
    colored_print("This is a normal message")

    # Using end argument
    colored_print("Loading", Theme.INFO, end="")
    colored_print("...", end="")
    colored_print(" Done!", Theme.SUCCESS)

    # Multi-colored text in one line
    colored_print(
        [
            ("Error: ", Theme.ERROR),
            ("File ", None),
            ("config.json", Theme.HIGHLIGHT),
            (" not found", Theme.WARNING),
        ]
    )

    colored_print(
        [
            ("Status: ", Theme.INFO),
            ("OK", Theme.SUCCESS),
            (" | Processed: ", None),
            ("42", Theme.HIGHLIGHT),
            (" items", None),
        ]
    )
