"""CLI binding for shared semantic configuration and candidate validation."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import cast

from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.parsing import InputError, mapping, strict_yaml
from agentic_ml.planning.paths import ProjectAccess, relative_path
from agentic_ml.validation import (
    CandidateRequest,
    CandidateResult,
    ConfigurationRequest,
    ConfigurationResult,
    ValidationError,
    inspect_validation,
    validate_candidate,
    validate_configuration,
)
from agentic_ml.validation.checks import bounded, reject, schema


def add_commands(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    """Register validation commands with explicit project-root binding."""
    for name, actions in (
        ("config", ("validate", "inspect")),
        ("candidate", ("validate",)),
    ):
        parent = commands.add_parser(name, help="Validate semantic experiment inputs")
        subcommands = parent.add_subparsers(dest="validation_action", required=True)
        for action in actions:
            command = subcommands.add_parser(action)
            command.add_argument("--project-root", required=True, type=Path)
            if name == "config" and action == "validate":
                command.add_argument("--plan-id", required=True)
                command.add_argument("--registry", type=Path)
            else:
                command.add_argument("--validation-id", required=True)
            if name == "candidate":
                command.add_argument("--candidate", type=Path, required=True)


def candidate(args: argparse.Namespace) -> CandidateResult:
    """Read a bounded candidate file and invoke the public validation interface."""
    access = ProjectAccess(args.project_root)
    try:
        path = relative_path(str(args.candidate))
        raw, marks = strict_yaml(access.read(path), path)
        bounded(raw)
        if isinstance(raw, dict) and raw.get("schema_version") != "1.0":
            reject(
                "unsupported_version",
                "schema_version",
                "Use validation schema version 1.0.",
                path,
            )
        schema(raw, "candidate", "invalid_candidate")
        value = mapping(raw)
        result = validate_candidate(
            CandidateRequest(
                args.project_root,
                args.validation_id,
                str(value["algorithm"]),
                mapping(value["parameters"]),
            )
        )
        access.recheck()
        diagnostics = []
        for item in result.diagnostics:
            if not item.source_path and (
                item.field == "algorithm" or item.field.startswith("parameters.")
            ):
                mark = marks.get(item.field)
                item = replace(
                    item,
                    source_path=path,
                    line=None if mark is None else mark[0],
                    column=None if mark is None else mark[1],
                )
            diagnostics.append(item)
        return replace(result, diagnostics=tuple(diagnostics))
    finally:
        access.close()


def dispatch(args: argparse.Namespace) -> None:
    """Emit one versioned JSON outcome and distinguish operational failures."""
    result: ConfigurationResult | CandidateResult
    try:
        if args.command == "candidate":
            result = candidate(args)
        elif args.validation_action == "inspect":
            result = inspect_validation(
                project_root=args.project_root, validation_id=args.validation_id
            )
        else:
            result = validate_configuration(
                ConfigurationRequest(args.project_root, args.plan_id, args.registry)
            )
    except InputError as error:
        if args.command == "candidate":
            result = CandidateResult(
                "blocked", args.validation_id, "", None, None, (error.diagnostic,)
            )
        else:
            result = ConfigurationResult("blocked", None, None, (error.diagnostic,))
    except (ValidationError, OSError) as error:
        code = error.code if isinstance(error, ValidationError) else "validation_io"
        print(
            json.dumps(
                {
                    "code": code,
                    "message": "Unable to complete validation; review project access and storage.",
                }
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from error
    output = cast(dict[str, JSONValue], asdict(result))
    output["schema_version"] = "1.0"
    print(json.dumps(output, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if result.status == "valid" else 2)
