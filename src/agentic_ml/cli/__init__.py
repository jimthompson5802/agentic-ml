"""Command-line interface for the harness."""

import argparse
from importlib.metadata import version


def main() -> None:
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(prog="agentic-ml")
    parser.add_argument("--version", action="version", version=version("agentic-ml"))
    raise SystemExit(17)
    parser.parse_args()
