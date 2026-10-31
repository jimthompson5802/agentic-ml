"""Command-line interface for the harness."""

import argparse
import sys
from importlib.metadata import version
from pathlib import Path

from agentic_ml.initialization import (
    InitializationError,
    InitOptions,
    initialize_project,
)


def main() -> None:
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(prog="agentic-ml")
    parser.add_argument("--version", action="version", version=version("agentic-ml"))
    commands = parser.add_subparsers(dest="command")
    init = commands.add_parser("init", help="Create draft experiment scaffolding")
    init.add_argument("--project-root", type=Path, default=Path.cwd())
    init.add_argument("--experiment", default="initial")
    init.add_argument("--package-name")
    for flag in ("dvc-store", "mlflow-backend", "artifact-store", "state-store"):
        init.add_argument("--" + flag, type=Path)
    args = parser.parse_args()
    if args.command == "init":
        try:
            result = initialize_project(
                InitOptions(
                    project_root=args.project_root,
                    experiment=args.experiment,
                    package_name=args.package_name,
                    dvc_store=args.dvc_store,
                    mlflow_backend=args.mlflow_backend,
                    artifact_store=args.artifact_store,
                    state_store=args.state_store,
                )
            )
        except InitializationError as error:
            print(f"Initialization failed at {error.stage}: {error}", file=sys.stderr)
            print(error.recovery, file=sys.stderr)
            raise SystemExit(1) from error
        for label, paths in (
            ("Created", result.created),
            ("Updated", result.updated),
            ("Unchanged", result.unchanged),
        ):
            for path in paths:
                print(f"{label}: {path}")
        if result.setup_pending:
            print("Setup pending: " + ", ".join(result.setup_pending))
        else:
            print(
                "Initialization complete; data access, agent authentication and approval presentation remain unconfigured."
            )
