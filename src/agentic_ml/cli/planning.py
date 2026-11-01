"""CLI dispatch for versioned declarative experiment planning."""

from __future__ import annotations

import argparse
import json
import stat
import sys
from dataclasses import asdict
from pathlib import Path

from agentic_ml.approvals import (
    ApprovalError,
    ApprovalRequest,
    RevocationRequest,
    approve_plan,
    revoke_approval,
)
from agentic_ml.planning import (
    PlanningError,
    ResolveRequest,
    inspect_plan,
    resolve_plan,
    verify_plan,
)
from agentic_ml.planning.models import PlanInspection, PlanResult


def add_commands(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Register plan resolution, inspection and verification commands."""
    plan = commands.add_parser("plan", help="Resolve and verify declarative inputs")
    actions = plan.add_subparsers(dest="plan_action", required=True)
    for name in ("resolve", "inspect", "verify", "approve", "revoke-approval"):
        command = actions.add_parser(name)
        command.add_argument("--project-root", type=Path)
        if name == "resolve":
            command.add_argument("--experiment", type=Path, required=True)
        else:
            command.add_argument("--plan", required=True)
        if name == "verify":
            command.add_argument("--check-current", action="store_true")
        if name in ("approve", "revoke-approval"):
            command.add_argument("--reviewer", required=True)
            command.add_argument("--reason", required=True)
        if name == "revoke-approval":
            command.add_argument("--approval", required=True)


def discover_root() -> Path:
    """Find the nearest project markers without falling back from invalid input."""
    current = Path.cwd()
    for path in (current, *current.parents):
        try:
            project = (path / "project.yaml").lstat()
            git = (path / ".git").lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISREG(project.st_mode) and (
            stat.S_ISREG(git.st_mode) or stat.S_ISDIR(git.st_mode)
        ):
            return path
    raise PlanningError(
        "project_not_found", "No project root found; provide --project-root."
    )


def dispatch(args: argparse.Namespace) -> None:
    """Emit a versioned JSON result and contract-defined exit status."""
    try:
        root = args.project_root if args.project_root is not None else discover_root()
        if args.plan_action in ("approve", "revoke-approval"):
            record = (
                approve_plan(
                    ApprovalRequest(root, args.plan, args.reviewer, args.reason)
                )
                if args.plan_action == "approve"
                else revoke_approval(
                    RevocationRequest(
                        root, args.plan, args.approval, args.reviewer, args.reason
                    )
                )
            )
            print(
                json.dumps(
                    asdict(record), sort_keys=True, ensure_ascii=False, allow_nan=False
                )
            )
            return
        result: PlanResult | PlanInspection
        if args.plan_action == "resolve":
            result = resolve_plan(ResolveRequest(root, args.experiment))
        elif args.plan_action == "inspect":
            result = inspect_plan(project_root=root, plan_id=args.plan)
        else:
            result = verify_plan(
                project_root=root, plan_id=args.plan, check_current=args.check_current
            )
        output = {"schema_version": "1.0", **asdict(result)}
        print(json.dumps(output, sort_keys=True, ensure_ascii=False, allow_nan=False))
        if result.status == "blocked":
            print("Planning blocked; review JSON diagnostics.", file=sys.stderr)
            raise SystemExit(2)
    except (PlanningError, ApprovalError) as error:
        print(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "plan_id": None,
                    "status": "blocked",
                    "diagnostics": [
                        {
                            "code": error.code,
                            "field": "",
                            "source_path": "",
                            "line": None,
                            "column": None,
                            "message": str(error),
                        }
                    ],
                }
            )
        )
        print(str(error), file=sys.stderr)
        raise SystemExit(
            2 if isinstance(error, ApprovalError) and not error.operational else 3
        ) from error
