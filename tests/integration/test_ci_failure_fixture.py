"""Temporary hosted CI failure fixture."""


def test_ci_reports_failed_assertion() -> None:
    """A deliberately failing assertion makes the CI test step fail."""
    assert 1 == 2
