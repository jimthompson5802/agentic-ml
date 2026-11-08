"""Independent installed-project assessment and partition oracles."""

import argparse
import hashlib
import importlib.util
import json
import sys
from collections.abc import Callable
from functools import partial
from importlib.metadata import version
from pathlib import Path
from typing import Any, cast

import pandas as pd

import agentic_ml
from agentic_ml.data_assessment import assess_data
from agentic_ml.data_quality import DataQualityError, run_validated_step
from agentic_ml.extraction import extract_data
from agentic_ml.splitting import create_partitions


def rejects(error: type[Exception], operation: Callable[[], object]) -> None:
    """Require the declared public exception without changing its criteria."""
    try:
        operation()
    except error as failure:
        assert str(failure)
    else:
        raise AssertionError(f"Expected {error.__name__}")


def assessment_cases() -> None:
    """Check literal statistics, scalar policies and invalid inputs."""
    frame = pd.DataFrame(
        {"value": [1.0, 3.0, 5.0, None], "label": ["A", "A", "B", None]}
    )
    before = frame.copy(deep=True)
    report = assess_data(frame, target="label")
    columns = cast(list[dict[str, Any]], report["columns"])
    assert report["row_count"] == 4
    assert columns[0]["missing_count"] == 1
    assert columns[0]["missing_rate"] == 0.25
    assert columns[0]["summary"] == {
        "count": 3.0,
        "mean": 3.0,
        "std": 2.0,
        "min": 1.0,
        "25%": 2.0,
        "50%": 3.0,
        "75%": 4.0,
        "max": 5.0,
    }
    assert report["target_balance"] == [
        {"value": "A", "count": 2, "proportion": 2 / 3},
        {"value": "B", "count": 1, "proportion": 1 / 3},
    ]
    assert columns[1]["missing_count"] == 1
    json.dumps(report, allow_nan=False)
    pd.testing.assert_frame_equal(frame, before)
    for values in ([], [None], [7]):
        result = assess_data(
            pd.DataFrame({"x": pd.Series(values, dtype="Int64")}), target="x"
        )
        column = cast(list[dict[str, Any]], result["columns"])[0]
        assert column["summary"]["std"] is None
        assert column["summary"]["count"] == (1 if values == [7] else 0)
        assert column["missing_rate"] == (
            None if not values else 1.0 if values == [None] else 0.0
        )
        json.dumps(result, allow_nan=False)
    typed = pd.DataFrame(
        {
            "flag": pd.Series([True, False, None], dtype="boolean"),
            "label": pd.Categorical(
                ["B", "B", None], categories=["A", "B", "C"], ordered=True
            ),
            "when": pd.to_datetime(
                pd.Series(["2024-01-01T00:00:00Z", "2024-01-01T00:00:00Z", None])
            ),
        }
    )
    result = assess_data(typed, target="label")
    entries = cast(list[dict[str, Any]], result["columns"])
    assert entries[0]["frequencies"] == [
        {"value": True, "count": 1, "proportion": 0.5},
        {"value": False, "count": 1, "proportion": 0.5},
    ]
    assert result["target_balance"] == [
        {"value": "A", "count": 0, "proportion": 0.0},
        {"value": "B", "count": 2, "proportion": 1.0},
        {"value": "C", "count": 0, "proportion": 0.0},
    ]
    assert entries[2]["frequencies"] == [
        {"value": "2024-01-01T00:00:00+00:00", "count": 2, "proportion": 1.0}
    ]
    infinite = assess_data(
        pd.DataFrame({"x": [float("inf"), float("-inf")]}), target="x"
    )
    assert [
        entry["value"]
        for entry in cast(list[dict[str, Any]], infinite["target_balance"])
    ] == ["Infinity", "-Infinity"]
    json.dumps(infinite, allow_nan=False)
    unsupported_columns: list[list[object]] = [
        [{}],
        [1, "x"],
        [1j],
        [pd.Timedelta(days=1)],
    ]
    for unsupported in unsupported_columns:
        rejects(
            TypeError,
            partial(assess_data, pd.DataFrame({"x": unsupported}), target="x"),
        )
    rejects(ValueError, partial(assess_data, frame, target="absent"))


def partition_cases(root: Path, project: Any) -> list[dict[str, object]]:
    """Check fixed seeded oracles, supplied protocols and independent identity."""
    frame = pd.DataFrame({"id": range(5), "label": list("ABCDE")}, index=range(10, 15))
    before = frame.copy(deep=True)
    records = []
    for layout, expected, extra in (
        ("train_test", {"train": [2, 0, 3], "test": [1, 4]}, {}),
        (
            "train_validation_test",
            {"train": [0, 3], "validation": [2], "test": [1, 4]},
            {"validation_size": 0.2},
        ),
    ):
        parts, record = create_partitions(
            frame,
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            seed=42,
            test_size=0.4,
            **cast(dict[str, Any], extra),
        )
        assert record["memberships"] == expected
        assert list(parts) == list(expected)
        for name, ids in expected.items():
            assert parts[name]["label"].tolist() == ["ABCDE"[i] for i in ids]
            assert parts[name].index.tolist() == [10 + i for i in ids]
        saved = project.save_load(root / f"{layout}.json", record)
        restored, current = create_partitions(
            frame,
            row_id="id",
            target="label",
            layout=saved["layout"],
            memberships=saved["memberships"],
        )
        assert current["method"] == "supplied" and current["source"] == record["source"]
        for name in parts:
            pd.testing.assert_frame_equal(parts[name], restored[name])
        source = cast(dict[str, Any], record["source"])
        payload = frame.copy()
        payload.attrs = {}
        assert (
            source["sha256"]
            == hashlib.sha256(
                payload.to_parquet(engine="pyarrow", index=False, compression=None)
            ).hexdigest()
        )
        _, reindexed = create_partitions(
            frame.reset_index(drop=True),
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            memberships=expected,
        )
        assert reindexed["source"] == source
        variants = [
            frame.assign(label=list("XBCDE")),
            frame.astype({"id": "int32"}),
            frame.iloc[::-1],
            frame.assign(id=[0, 1, 2, 3, 8]),
        ]
        for variant in variants[:3]:
            _, changed = create_partitions(
                variant,
                row_id="id",
                target="label",
                layout=cast(Any, layout),
                memberships=expected,
            )
            assert cast(dict[str, Any], changed["source"])["sha256"] != source["sha256"]
        rejects(
            ValueError,
            partial(
                create_partitions,
                variants[3],
                row_id="id",
                target="label",
                layout=cast(Any, layout),
                memberships=expected,
            ),
        )
        records.append(record)
    pd.testing.assert_frame_equal(frame, before)
    for layout, members in (
        ("train_test", {"train": [1, 2, 3, 4], "test": [5, 6]}),
        (
            "train_validation_test",
            {"train": [1, 2], "validation": [3, 4], "test": [5, 6]},
        ),
    ):
        data = pd.DataFrame(
            {
                "id": range(1, 7),
                "label": list("ABABAB"),
                "time": pd.date_range("2024-01-01", periods=6),
                "group": ["a", "a", "b", "b", "c", "c"],
            }
        )
        for kind, column in (("time", "time"), ("group", "group")):
            parts, record = create_partitions(
                data,
                row_id="id",
                target="label",
                layout=cast(Any, layout),
                memberships=members,
                protocol={"kind": kind, "column": column},
            )
            assert record["memberships"] == members
            assert record["protocol"] == {"kind": kind, "column": column}
            names = list(parts)
            for left, right in zip(names, names[1:], strict=False):
                assert parts[left]["time"].max() < parts[right]["time"].min()
                assert not set(parts[left]["group"]) & set(parts[right]["group"])
            saved = project.save_load(root / f"{layout}-{kind}.json", record)
            restored, _ = create_partitions(
                data,
                row_id="id",
                target="label",
                layout=saved["layout"],
                memberships=saved["memberships"],
                protocol=saved["protocol"],
            )
            for name, ids in members.items():
                assert restored[name]["id"].tolist() == ids
            records.append(record)
        invalid = [
            dict(members, train=[1, 1]),
            dict(members, train=[1, 7]),
            dict(members, train=[]),
            {"train": [1, 2]},
            dict(members, extra=[1]),
        ]
        invalid += [
            dict(members, train=members["train"] + [5]),
            dict(members, train=members["train"][:-1]),
        ]
        for selected in invalid:
            rejects(
                ValueError,
                partial(
                    create_partitions,
                    data,
                    row_id="id",
                    target="label",
                    layout=cast(Any, layout),
                    memberships=selected,
                ),
            )
    balanced = pd.DataFrame({"id": range(20), "label": ["A", "B"] * 10})
    for layout, extra, counts in (
        ("train_test", {}, {"train": 8, "test": 2}),
        (
            "train_validation_test",
            {"validation_size": 0.2},
            {"train": 6, "validation": 2, "test": 2},
        ),
    ):
        parts, _ = create_partitions(
            balanced,
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            seed=42,
            test_size=0.2,
            stratify=True,
            **cast(dict[str, Any], extra),
        )
        for name, count in counts.items():
            assert parts[name]["label"].value_counts().to_dict() == {
                "A": count,
                "B": count,
            }
            assert parts[name]["label"].tolist() == [
                "AB"[i % 2] for i in parts[name]["id"]
            ]
    for invalid_settings in (
        {"test_size": 0.0},
        {"test_size": float("nan")},
        {"validation_size": 0.2},
        {"shuffle": False, "stratify": True},
        {"protocol": {"kind": "time", "column": "id"}},
    ):
        settings: dict[str, Any] = {"seed": 42, "test_size": 0.4, **invalid_settings}
        rejects(
            ValueError,
            partial(
                create_partitions,
                frame,
                row_id="id",
                target="label",
                layout="train_test",
                **settings,
            ),
        )
    invalid_sources: list[tuple[list[object], type[Exception]]] = [
        ([1, 1, 2, 3, 4], ValueError),
        ([True] * 5, TypeError),
        ([1, "x", 2, 3, 4], TypeError),
        ([1, 2, 3, 4, None], ValueError),
    ]
    for invalid_ids, error in invalid_sources:
        rejects(
            error,
            partial(
                create_partitions,
                frame.assign(id=pd.Series(invalid_ids, index=frame.index)),
                row_id="id",
                target="label",
                layout="train_test",
                seed=42,
                test_size=0.4,
            ),
        )
    rejects(
        ValueError,
        partial(
            create_partitions,
            frame.iloc[:1],
            row_id="id",
            target="label",
            layout="train_test",
            seed=42,
            test_size=0.4,
        ),
    )
    rounded, _ = create_partitions(
        frame, row_id="id", target="label", layout="train_test", seed=42, test_size=0.3
    )
    assert len(rounded["test"]) == 2 and len(rounded["train"]) == 3
    for invalid_classes in (
        frame.assign(label=list("AAAAB")),
        frame.assign(label=pd.Series(["A", "B", None, "A", "B"], index=frame.index)),
    ):
        rejects(
            ValueError,
            partial(
                create_partitions,
                invalid_classes,
                row_id="id",
                target="label",
                layout="train_test",
                seed=42,
                test_size=0.4,
                stratify=True,
            ),
        )
    rejects(
        ValueError,
        partial(
            create_partitions,
            frame.iloc[:2],
            row_id="id",
            target="label",
            layout="train_validation_test",
            seed=42,
            test_size=0.4,
            validation_size=0.2,
        ),
    )
    return records


def main() -> None:
    """Run public behavior through a normally installed independent project."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--project-code", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace
    root.mkdir(parents=True)
    code = root / "project_assessment_splits.py"
    code.write_bytes(args.project_code.read_bytes())
    spec = importlib.util.spec_from_file_location("project_assessment_splits", code)
    assert spec is not None and spec.loader is not None
    project = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(project)
    package = Path(agentic_ml.__file__ or "").resolve()
    assert package.is_relative_to(Path(sys.prefix).resolve())
    assert "site-packages" in package.parts and sys.prefix != sys.base_prefix
    assert importlib.util.find_spec("pytest") is None
    assert Path.cwd() != root
    assessment_cases()
    records = partition_cases(root, project)
    (root / "data.csv").write_text("id,label\n0,A\n1,B\n2,A\n3,B\n4,A\n")
    frame, extraction = extract_data(
        project.extract,
        project_root=root,
        sources={"data": Path("data.csv")},
        destination=Path("extracted"),
        code_paths=[Path(code.name)],
    )
    sentinel = root / "prepared"
    rule = {"id": "rows", "kind": "row_count", "min": 6}
    rejects(
        DataQualityError,
        partial(
            run_validated_step,
            frame,
            project.prepare,
            rules=[rule],
            settings={"sentinel": str(sentinel)},
        ),
    )
    assert not sentinel.exists()
    for rules, status in (
        ([], "not_checked"),
        ([dict(rule, required=False)], "failed"),
        ([dict(rule, min=5)], "passed"),
    ):
        output, quality = run_validated_step(
            frame, project.prepare, rules=rules, settings={"sentinel": str(sentinel)}
        )
        assert sentinel.read_text() == "prepared" and quality["status"] == status
        assert output["assessment"]["row_count"] == 5
        assert output["record"]["memberships"] == {"train": [2, 0, 3], "test": [1, 4]}
        sentinel.unlink()
    identity = {
        "package": str(package),
        "python": sys.version,
        "prefix": sys.prefix,
        "working_directory": str(Path.cwd()),
        "project_code": str(code),
        "versions": {
            name: version(name)
            for name in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
        },
        "records": records,
        "extraction": extraction,
        "criteria": ["US-12-AC-02", "US-12-AC-03"],
        "sentinels": ["required_blocked", "passed", "advisory", "not_checked"],
    }
    (root / "identity.json").write_text(json.dumps(identity, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
