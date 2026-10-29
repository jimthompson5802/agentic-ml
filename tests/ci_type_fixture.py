"""Temporary hosted type failure fixture."""


def invalid_return() -> int:
    """Return a deliberately incompatible value."""
    return "wrong-type"
