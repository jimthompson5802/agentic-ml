"""Strict, bounded declarative input parsing with source diagnostics."""

import json
import math
import re
from dataclasses import replace
from importlib.resources import files
from typing import NoReturn, cast

import yaml
from jsonschema import Draft202012Validator
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

from agentic_ml.planning.models import Diagnostic, JSONValue


class InputError(Exception):
    """Carry a safe source-located validation diagnostic."""

    def __init__(self, diagnostic: Diagnostic) -> None:
        """Initialize a blocking input problem."""
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


def fail(
    code: str, field: str, source: str, line: int = 1, column: int = 1
) -> NoReturn:
    """Reject a declarative input without printing its contents."""
    raise InputError(
        Diagnostic(
            code,
            field,
            source,
            line,
            column,
            "Invalid or unresolved input; review the indicated field.",
        )
    )


def mapping(value: JSONValue) -> dict[str, JSONValue]:
    """Return an already validated JSON mapping."""
    if not isinstance(value, dict):
        raise ValueError("Expected mapping")
    return value


def sequence(value: JSONValue) -> list[JSONValue]:
    """Return an already validated JSON sequence."""
    if not isinstance(value, list):
        raise ValueError("Expected list")
    return value


def strict_yaml(
    content: bytes, source: str
) -> tuple[JSONValue, dict[str, tuple[int, int]]]:
    """Parse JSON-compatible YAML without duplicate keys, aliases or tags."""
    marks: dict[str, tuple[int, int]] = {"": (1, 1)}
    try:
        text = content.decode("utf-8")
        if len(content) > 1048576 or text.startswith("\ufeff"):
            fail("invalid_input", "", source)
        depth = 0
        for event in yaml.parse(text):
            if isinstance(event, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
                depth += 1
                if depth > 20:
                    fail(
                        "input_limit",
                        "",
                        source,
                        1 if event.start_mark is None else event.start_mark.line + 1,
                        1 if event.start_mark is None else event.start_mark.column + 1,
                    )
            elif isinstance(event, (yaml.MappingEndEvent, yaml.SequenceEndEvent)):
                depth -= 1
            if (
                isinstance(event, yaml.AliasEvent)
                or getattr(event, "anchor", None)
                or getattr(event, "tag", None)
            ):
                fail(
                    "invalid_yaml",
                    "",
                    source,
                    event.start_mark.line + 1,
                    event.start_mark.column + 1,
                )
        node = yaml.compose(text)

        def walk(current: Node | None, path: str, depth: int) -> None:
            if current is None or depth > 20:
                fail("invalid_yaml", path, source)
            marks[path] = (current.start_mark.line + 1, current.start_mark.column + 1)
            if isinstance(current, MappingNode):
                seen: set[str] = set()
                for key, value in current.value:
                    if (
                        not isinstance(key, ScalarNode)
                        or key.tag != "tag:yaml.org,2002:str"
                        or key.value in seen
                        or key.value == "<<"
                    ):
                        fail(
                            "duplicate_or_invalid_key",
                            path,
                            source,
                            key.start_mark.line + 1,
                            key.start_mark.column + 1,
                        )
                    seen.add(key.value)
                    walk(value, f"{path}.{key.value}".strip("."), depth + 1)
            elif isinstance(current, SequenceNode):
                for index, item in enumerate(current.value):
                    walk(item, f"{path}.{index}".strip("."), depth + 1)
            elif not isinstance(current, ScalarNode) or current.tag not in {
                "tag:yaml.org,2002:" + t
                for t in ("str", "int", "float", "bool", "null")
            }:
                fail("invalid_yaml", path, source)

        walk(node, "", 0)
        value = cast(JSONValue, yaml.safe_load(text))

        def finite(item: JSONValue, path: str) -> None:
            if (
                isinstance(item, float)
                and not math.isfinite(item)
                or type(item) is int
                and abs(item) > 9007199254740991
            ):
                fail("invalid_number", path, source, *marks.get(path, (1, 1)))
            if isinstance(item, dict):
                for key, child in item.items():
                    finite(child, f"{path}.{key}".strip("."))
            elif isinstance(item, list):
                for index, child in enumerate(item):
                    finite(child, f"{path}.{index}".strip("."))

        finite(value, "")
        return value, marks
    except (yaml.YAMLError, UnicodeError) as error:
        mark = getattr(error, "problem_mark", None)
        fail(
            "invalid_yaml",
            "",
            source,
            1 if mark is None else mark.line + 1,
            1 if mark is None else mark.column + 1,
        )
        raise AssertionError("unreachable") from error


def validate(
    value: JSONValue, schema: str, source: str, marks: dict[str, tuple[int, int]]
) -> None:
    """Validate a value against the installed versioned schema."""
    definition = json.loads(
        files("agentic_ml").joinpath(f"schemas/planning/1.0/{schema}.json").read_bytes()
    )
    errors = list(Draft202012Validator(definition).iter_errors(value))
    if errors:
        error = errors[0]
        path = ".".join(str(part) for part in error.absolute_path)
        fail("invalid_field", path, source, *marks.get(path, (1, 1)))


def parse_brief(
    content: bytes, source: str
) -> tuple[dict[str, JSONValue], dict[str, tuple[int, int]]]:
    """Read exactly six ordered Markdown sections with YAML decisions."""
    try:
        text = content.decode("utf-8").replace("\r\n", "\n")
    except UnicodeError as error:
        fail("invalid_brief", "", source)
        raise AssertionError("unreachable") from error
    if len(content) > 1048576 or not re.match(r"\A# Experiment: [^\n]+\n", text):
        fail("invalid_brief", "", source)
    sections = re.split(r"(?m)^## ", text)
    if len(sections) != 7 or any(
        line.strip() and not line.startswith("> Note: ")
        for line in sections[0].splitlines()[1:]
    ):
        fail("invalid_brief", "", source)
    result: dict[str, JSONValue] = {}
    marks: dict[str, tuple[int, int]] = {}
    offset = len(sections[0].splitlines())
    for title, section in zip(
        ("Objective", "Data", "Features", "Evaluation", "Algorithms", "Budget"),
        sections[1:],
        strict=True,
    ):
        lines = section.splitlines()
        if not lines or lines[0] != title:
            fail("invalid_brief", "", source, offset + 1)
        body = "\n".join(lines[1:])
        match = re.fullmatch(
            r"((?:\n|> Note: [^\n]*\n)*)```yaml\n(.*?)\n```((?:\n|\n> Note: [^\n]*)*)",
            body,
            re.DOTALL,
        )
        if match is None:
            fail("invalid_brief", title.lower(), source, offset + 1)
        start = offset + 2 + match[1].count("\n")
        try:
            value, positions = strict_yaml(match[2].encode(), source)
        except InputError as error:
            diagnostic = error.diagnostic
            raise InputError(
                replace(
                    diagnostic,
                    line=None if diagnostic.line is None else start + diagnostic.line,
                )
            ) from error
        result[title.lower()] = value
        for path, (line, column) in positions.items():
            marks[(title.lower() + "." + path).rstrip(".")] = (start + line, column)
        offset += len(lines)
    validate(result, "brief", source, marks)
    return result, marks


def derive_decisions(
    brief: dict[str, JSONValue], source: str, marks: dict[str, tuple[int, int]]
) -> tuple[
    dict[str, JSONValue], list[JSONValue], list[JSONValue], tuple[Diagnostic, ...]
]:
    """Separate explicit author values from pending delegated choices."""
    effective: dict[str, JSONValue] = {}
    decisions: list[JSONValue] = []
    pending: list[JSONValue] = []
    diagnostics: list[Diagnostic] = []
    for section, raw in brief.items():
        resolved: dict[str, JSONValue] = {}
        for key, value in mapping(raw).items():
            field = section + "." + key
            line, column = marks[field]
            delegated = isinstance(value, dict) and "delegate" in value
            selected = (
                value.get("proposal")
                if delegated and isinstance(value, dict)
                else value
            )
            resolved[key] = selected
            decisions.append(
                {
                    "field": field,
                    "origin": "delegated" if delegated else "explicit",
                    "source_path": source,
                    "line": line,
                    "column": column,
                    "original": value,
                    "proposed": selected if delegated else None,
                    "effective": selected,
                    "rationale": value.get("rationale")
                    if delegated and isinstance(value, dict)
                    else None,
                }
            )
            if delegated:
                pending.append(field)
                diagnostics.append(
                    Diagnostic(
                        "pending_decision" if selected is None else "approval_required",
                        field,
                        source,
                        line,
                        column,
                        "An explicit experiment approval is required before use.",
                    )
                )
        effective[section] = resolved
    features = mapping(effective["features"])
    include, exclude = features["include"], features["exclude"]
    if (
        isinstance(include, list)
        and isinstance(exclude, list)
        and set(cast(list[str], include)) & set(cast(list[str], exclude))
    ):
        fail(
            "conflicting_features",
            "features.exclude",
            source,
            *marks["features.exclude"],
        )
    evaluation = mapping(effective["evaluation"])
    split = evaluation["split"]
    if isinstance(split, dict):
        validation_fraction = cast(float, split["validation_fraction"])
        test_fraction = cast(float, split["test_fraction"])
        if (
            validation_fraction + test_fraction >= 1
            or (split["strategy"] == "time") != isinstance(split["time_column"], str)
            or (split["strategy"] == "group") != isinstance(split["group_column"], str)
            or split["strategy"] == "stratified"
            and mapping(effective["data"])["task_type"] not in (None, "classification")
        ):
            fail(
                "conflicting_split",
                "evaluation.split",
                source,
                *marks["evaluation.split"],
            )
    budget = mapping(effective["budget"])
    cost_raw = mapping(brief["budget"])["max_cost"]
    currency_raw = mapping(brief["budget"])["currency"]
    if (
        not isinstance(cost_raw, dict)
        and not isinstance(currency_raw, dict)
        and (budget["max_cost"] is None) != (budget["currency"] is None)
    ):
        fail("conflicting_budget", "budget.max_cost", source, *marks["budget.max_cost"])
    algorithms = mapping(effective["algorithms"])
    if (
        algorithms["mode"] == "use"
        and isinstance(algorithms["allowed"], list)
        and len(algorithms["allowed"]) != 1
    ):
        fail(
            "conflicting_algorithms",
            "algorithms.allowed",
            source,
            *marks["algorithms.allowed"],
        )
    return effective, decisions, pending, tuple(diagnostics)
