"""Check installed quality APIs through independent project code and outcomes."""

import argparse
import copy
import importlib.util
import json
import sys
from importlib.metadata import version
from pathlib import Path
from typing import cast

import pandas as pd

import agentic_ml
from agentic_ml.data_quality import DataQualityError, run_validated_step, validate_data
from agentic_ml.extraction import extract_data


def main() -> None:
    """Verify both criterion families without contributor imports or tools."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--project-code", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace
    root.mkdir(parents=True)
    code = root / "project_data_quality.py"
    code.write_bytes(args.project_code.read_bytes())
    spec = importlib.util.spec_from_file_location("project_data_quality", code)
    assert spec is not None and spec.loader is not None
    project = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(project)
    package = Path(agentic_ml.__file__ or "").resolve()
    assert package.is_relative_to(Path(sys.prefix).resolve())
    assert "site-packages" in package.parts and sys.prefix != sys.base_prefix
    assert importlib.util.find_spec("pytest") is None
    assert Path.cwd() != root
    (root / "people.csv").write_text("id,age,group\n1,20,A\n2,35,B\n3,40,A\n4,50,C\n")
    frame, extraction = extract_data(
        project.extract,
        project_root=root,
        sources={"people": Path("people.csv")},
        destination=Path("extracted"),
        code_paths=[Path(code.name)],
    )
    assert list(frame.itertuples(index=False, name=None)) == [
        (1, 20, "A"),
        (2, 35, "B"),
        (3, 40, "A"),
        (4, 50, "C"),
    ]
    rules = project.RULES
    original_rules = copy.deepcopy(rules)
    report = validate_data(frame, rules=rules)
    checks = cast(list[dict[str, object]], report["checks"])
    assert report["status"] == "passed" and report["blocked"] is False
    assert [check["actual"] for check in checks] == [
        {"missing": [], "unexpected": []},
        {"dtypes": {"id": "int64", "age": "int64"}},
        {"count": 4},
        {"count": 0},
        {"count": 0},
        {"invalid_count": 0, "missing_count": 0},
        {"invalid_count": 0, "missing_count": 0},
    ]
    assert all(check["passed"] is True and check["message"] for check in checks)
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    # Each independently altered input exercises a separate declared rule family.
    variants = [
        frame.drop(columns="age"),
        frame.astype({"age": "float64"}),
        frame.iloc[:3].copy(),
        frame.astype({"age": "Int64"}),
        frame.copy(),
        frame.copy(),
        frame.copy(),
    ]
    variants[3].loc[0, "age"] = pd.NA
    variants[4].loc[1, "id"] = 1
    variants[5].loc[0, "age"] = 121
    variants[6].loc[0, "group"] = "Z"
    expected = [
        {"missing": ["age"], "unexpected": []},
        {"dtypes": {"id": "int64", "age": "float64"}},
        {"count": 3},
        {"count": 1},
        {"count": 1},
        {"invalid_count": 1, "missing_count": 0},
        {"invalid_count": 1, "missing_count": 0},
    ]
    failures = []
    for index, (variant, actual) in enumerate(zip(variants, expected, strict=True)):
        result = validate_data(variant, rules=[rules[index]])
        assert result["blocked"] is True and result["status"] == "failed"
        assert cast(list[dict[str, object]], result["checks"])[0]["actual"] == actual
        failures.append(result)
    sentinel = root / "consumed.txt"
    settings: dict[str, object] = {"sentinel": str(sentinel)}
    original = frame.copy(deep=True)
    for label, selected, data in [
        ("passed", rules, frame),
        ("advisory", [dict(rules[5], required=False)], variants[5]),
        ("not_checked", [], variants[5]),
    ]:
        output, checked = run_validated_step(
            data, project.consume, rules=selected, settings=settings
        )
        assert output == ([20, 35, 40, 50] if label == "passed" else [121, 35, 40, 50])
        assert sentinel.read_text() == str(output)
        assert checked["status"] == ("failed" if label == "advisory" else label)
        sentinel.unlink()
    pd.testing.assert_frame_equal(frame, original)
    assert settings == {"sentinel": str(sentinel)}
    try:
        run_validated_step(variants[5], project.consume, rules=rules, settings=settings)
    except DataQualityError as error:
        assert error.report == validate_data(variants[5], rules=rules)
        assert "age_bounds" in str(error)
    else:
        raise AssertionError("required failure did not block")
    assert not sentinel.exists()
    malformed = [{"id": "bad", "kind": "unknown"}]
    try:
        run_validated_step(frame, project.consume, rules=malformed, settings=settings)
    except ValueError:
        pass
    else:
        raise AssertionError("malformed rule accepted")
    assert not sentinel.exists()
    try:
        run_validated_step(frame, project.fail, rules=rules)
    except RuntimeError as error:
        assert error is project.PROJECT_ERROR
        assert any("validated" in note for note in error.__notes__)
    else:
        raise AssertionError("project exception lost")
    assert rules == original_rules
    identity = {
        "package": str(package),
        "python": sys.version,
        "prefix": sys.prefix,
        "working_directory": str(Path.cwd()),
        "project_code": str(code),
        "versions": {
            name: version(name) for name in ("agentic-ml", "pandas", "pyarrow")
        },
        "report": report,
        "rule_failures": failures,
        "extraction": extraction,
        "sentinels": ["passed", "advisory", "not_checked", "required_blocked"],
        "errors": ["malformed_rule", "original_project_exception"],
    }
    (root / "identity.json").write_text(json.dumps(identity, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
