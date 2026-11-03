"""Load contributor workspace support and assign verification schedules."""

import pytest

pytest_plugins = ["pytest_workspace_support"]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Assign new tests to phase checks and reject ambiguous schedules."""
    for item in items:
        phase = item.get_closest_marker("phase") is not None
        acceptance = item.get_closest_marker("story_acceptance") is not None
        if phase and acceptance:
            raise pytest.UsageError(f"Conflicting verification groups: {item.nodeid}")
        if not acceptance:
            item.add_marker(pytest.mark.phase)
