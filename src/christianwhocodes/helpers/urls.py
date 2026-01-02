def normalize_url_path(
    url: str, leading_slash: bool = False, trailing_slash: bool = True
) -> str:
    """
    Normalize URL format by ensuring consistent slash usage.

    Args:
        url: The URL string to normalize
        leading_slash: Whether the URL should start with a slash
        trailing_slash: Whether the URL should end with a slash

    Returns:
        Normalized URL string
    """
    if not url:
        return "/"

    # Remove multiple consecutive slashes
    while "//" in url:
        url = url.replace("//", "/")

    # Handle leading slash
    if leading_slash and not url.startswith("/"):
        url = "/" + url
    elif not leading_slash and url.startswith("/"):
        url = url.lstrip("/")

    # Handle trailing slash
    if trailing_slash and not url.endswith("/"):
        url = url + "/"
    elif not trailing_slash and url.endswith("/"):
        url = url.rstrip("/")

    return url
