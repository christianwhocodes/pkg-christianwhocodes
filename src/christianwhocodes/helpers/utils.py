import secrets
import string
from typing import Any, Iterable

from pyperclip import copy

from christianwhocodes.helpers.stdout import Text, print


def generate_random_string(
    length: int = 32,
    no_clipboard: bool = False,
    charset: str = string.ascii_letters + string.digits,
) -> str:
    """Generate a cryptographically secure random string and copy it to clipboard.

    Args:
        length: Length of the random string (default: 32).
        no_clipboard: If True, skip copying to clipboard (default: False).
        charset: Character set to use (default: alphanumeric).

    Returns:
        str: The generated random string.

    Example:
        >>> random_str = generate_random_string(16)
        Generated: aB3dEf7gHi9jKl2m
        Copied to clipboard!
        >>> random_str = generate_random_string(16, no_clipboard=True)
        Generated: nO5pQr8sT1uVw4xY
    """

    random_str = "".join(secrets.choice(charset) for _ in range(length))

    print(
        [
            ("Generated: ", Text.INFO),
            (random_str, Text.HIGHLIGHT),
        ]
    )

    # Copy to clipboard unless disabled
    if not no_clipboard:
        try:
            copy(random_str)
            print("Copied to clipboard!", Text.SUCCESS)
        except Exception as e:
            print(f"Could not copy to clipboard: {e}", Text.WARNING)

    return random_str


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Return the maximum string length among a list of `(value, display)` pairs.

    Args:
        choices: Iterable of (value, display) tuples.

    Returns:
        int: The maximum length of the value field.
    """
    return max(len(choice[0]) for choice in choices)
