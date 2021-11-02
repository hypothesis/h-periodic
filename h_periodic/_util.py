def asbool(value):
    """Return True if value is any of "t", "true", "y", etc (case-insensitive)."""
    return str(value).strip().lower() in ("t", "true", "y", "yes", "on", "1")
