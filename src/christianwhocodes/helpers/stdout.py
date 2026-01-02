from enum import StrEnum

from rich.console import Console
from rich.theme import Theme


class Text(StrEnum):
    """Rich color codes for use in styled output.

    Attributes:
        ERROR: Bold red styling for error messages.
        WARNING: Bold yellow styling for warning messages.
        SUCCESS: Bold green styling for success messages.
        INFO: Bold cyan styling for informational messages.
        DEBUG: Bold magenta styling for debug messages.
        HIGHLIGHT: Bold blue styling for highlighted text.
    """

    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
    DEBUG = "debug"
    HIGHLIGHT = "highlight"


THEME = Theme(
    {
        Text.ERROR: "bold red",
        Text.WARNING: "bold yellow",
        Text.SUCCESS: "bold green",
        Text.INFO: "bold cyan",
        Text.DEBUG: "bold magenta",
        Text.HIGHLIGHT: "bold blue",
    }
)

console = Console(theme=THEME)


def print(
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
        print("Error!", Theme.ERROR)
        print("Status: ", Theme.INFO, end="")
        print([("Error: ", Theme.ERROR), ("File not found", Theme.WARNING)])
    """
    if isinstance(text, list):
        # Multi-colored mode: text is a list of (text, color) tuples
        output = ""
        for segment_text, segment_color in text:
            if segment_color:
                output += f"[{segment_color}]{segment_text}[/{segment_color}]"
            else:
                output += segment_text
        console.print(output, end=end)
    else:
        # Single color mode
        if color:
            console.print(f"[{color}]{text}[/{color}]", end=end)
        else:
            console.print(text, end=end)


# Example usage
if __name__ == "__main__":
    # Single color examples
    print("This is an error message", Text.ERROR)
    print("This is a warning message", Text.WARNING)
    print("This is a success message", Text.SUCCESS)
    print("This is an info message", Text.INFO)
    print("This is a normal message")

    # Using end argument
    print("Loading", Text.INFO, end="")
    print("...", end="")
    print(" Done!", Text.SUCCESS)

    # Multi-colored text in one line
    print(
        [
            ("Error: ", Text.ERROR),
            ("File ", None),
            ("config.json", Text.HIGHLIGHT),
            (" not found", Text.WARNING),
        ]
    )

    print(
        [
            ("Status: ", Text.INFO),
            ("OK", Text.SUCCESS),
            (" | Processed: ", None),
            ("42", Text.HIGHLIGHT),
            (" items", None),
        ]
    )
