"""Verify the installed CLI through its public subprocess interface."""

import shutil
import subprocess
import sys
from importlib.metadata import distribution
from pathlib import Path


def test_version_reports_installed_distribution_version(tmp_path: Path) -> None:
    """The version command exits successfully and prints installed metadata."""
    assert shutil.which("agentic-ml") is not None, "Required CLI is not installed"
    expected_version = distribution("agentic-ml").version

    result = subprocess.run(
        ["agentic-ml", "--version"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == expected_version
    assert result.stderr == ""


def test_package_imports_from_outside_checkout(tmp_path: Path) -> None:
    """The installed public package imports without the checkout as cwd."""
    result = subprocess.run(
        [sys.executable, "-I", "-c", "import agentic_ml"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_help_uses_corrected_cli_name(tmp_path: Path) -> None:
    """Help identifies the command using its installed public name."""
    result = subprocess.run(
        ["agentic-ml", "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("usage: agentic-ml ")
    assert result.stderr == ""
