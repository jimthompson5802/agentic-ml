"""Load contributor workspace support and validate test classification."""

import pytest

pytest_plugins = ["pytest_workspace_support"]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Require explicit milestone or infrastructure classification before selection."""
    classifications = {f"milestone_{n}" for n in (0, 1, 2, 3, 4, 5, 6, 50, 99)}
    classifications.add("infrastructure")
    missing = [
        item.nodeid
        for item in items
        if not any(mark.name in classifications for mark in item.iter_markers())
    ]
    if missing:
        raise pytest.UsageError(
            "Missing test classification; add milestone_N or infrastructure markers:\n"
            + "\n".join(missing)
        )
