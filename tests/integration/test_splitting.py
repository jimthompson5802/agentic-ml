"""Public partition behavior for US-12-AC-03."""

import json
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest

from agentic_ml.splitting import create_partitions

pytestmark = pytest.mark.milestone_1


def test_seeded_two_way_literal_membership() -> None:
    """Native seed 42 retains exact row order and aligned targets."""
    frame = pd.DataFrame({"id": range(5), "label": list("ABCDE")}, index=range(10, 15))
    before = frame.copy(deep=True)
    parts, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        seed=42,
        test_size=0.4,
    )
    assert list(parts) == ["train", "test"]
    assert parts["train"]["id"].tolist() == [2, 0, 3]
    assert parts["test"]["id"].tolist() == [1, 4]
    assert parts["train"]["label"].tolist() == ["C", "A", "D"]
    assert parts["train"].index.tolist() == [12, 10, 13]
    assert record["layout"] == "train_test"
    assert record["memberships"] == {"train": [2, 0, 3], "test": [1, 4]}
    pd.testing.assert_frame_equal(frame, before)
    parts["train"].iloc[0, 1] = "changed"
    pd.testing.assert_frame_equal(frame, before)


@pytest.mark.parametrize(
    ("members", "error", "message"),
    [
        ({"train": [1, 2, 3], "test": [3, 4, 5, 6]}, ValueError, "overlap"),
        ({"train": [1, 1, 2, 3, 4], "test": [5, 6]}, ValueError, "duplicate"),
        ({"train": [1, 2, 3, 4], "test": [5, 7]}, ValueError, "unknown"),
        ({"train": [1, 2, 3, 4], "test": [5]}, ValueError, "coverage"),
        ({"train": [1, 2, 3, 4, 5, 6], "test": []}, ValueError, "nonempty"),
        ({"train": [1, 2, 3, 4]}, ValueError, "keys"),
        ({"train": [1, 2], "validation": [3, 4], "test": [5, 6]}, ValueError, "keys"),
        ({"training": [1, 2, 3, 4], "test": [5, 6]}, ValueError, "keys"),
        ({"train": [True, 2, 3, 4], "test": [5, 6]}, TypeError, "ID"),
        ({"train": [1.0, 2, 3, 4], "test": [5, 6]}, TypeError, "ID"),
        ({"train": ["1", 2, 3, 4], "test": [5, 6]}, TypeError, "ID"),
        ({"train": "1234", "test": [5, 6]}, TypeError, "sequence"),
        ([1, 2], TypeError, "memberships"),
    ],
)
def test_supplied_membership_errors(
    members: object, error: type[Exception], message: str
) -> None:
    """Invalid membership cannot silently omit, alias or duplicate rows."""
    with pytest.raises(error, match=message):
        create_partitions(
            pd.DataFrame({"id": range(1, 7), "label": list("ABABAB")}),
            row_id="id",
            target="label",
            layout="train_test",
            memberships=cast(Any, members),
        )


def test_seeded_three_way_literal_membership() -> None:
    """Reserve test first, then validation, with the reviewed native seed."""
    frame = pd.DataFrame({"id": range(5), "label": list("ABCDE")})
    parts, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        seed=42,
        test_size=0.4,
        validation_size=0.2,
    )
    assert list(parts) == ["train", "validation", "test"]
    assert record["memberships"] == {
        "train": [0, 3],
        "validation": [2],
        "test": [1, 4],
    }
    assert parts["validation"]["label"].tolist() == ["C"]


@pytest.mark.parametrize(
    ("changes", "error", "message"),
    [
        ({"layout": "other"}, ValueError, "layout"),
        ({"seed": None}, ValueError, "seed"),
        ({"seed": True}, TypeError, "seed"),
        ({"seed": -1}, ValueError, "seed"),
        ({"seed": 2**32}, ValueError, "seed"),
        ({"seed": 1.5}, TypeError, "seed"),
        ({"test_size": None}, ValueError, "test_size"),
        ({"test_size": True}, TypeError, "test_size"),
        ({"test_size": "0.4"}, TypeError, "test_size"),
        ({"test_size": float("nan")}, ValueError, "test_size"),
        ({"test_size": float("inf")}, ValueError, "test_size"),
        ({"test_size": 0.0}, ValueError, "test_size"),
        ({"test_size": 1.0}, ValueError, "test_size"),
        ({"validation_size": 0.2}, ValueError, "validation_size"),
        ({"layout": "train_validation_test"}, ValueError, "validation_size"),
        (
            {"layout": "train_validation_test", "validation_size": 0.6},
            ValueError,
            "sum",
        ),
        ({"shuffle": 1}, TypeError, "shuffle"),
        ({"stratify": 1}, TypeError, "stratify"),
        ({"protocol": {"kind": "supplied"}}, ValueError, "protocol"),
    ],
)
def test_generation_rejects_invalid_settings(
    changes: dict[str, object],
    error: type[Exception],
    message: str,
) -> None:
    """Reject incompatible settings without silently changing native behavior."""
    settings: dict[str, Any] = {
        "row_id": "id",
        "target": "label",
        "layout": "train_test",
        "seed": 42,
        "test_size": 0.4,
    }
    settings.update(changes)
    with pytest.raises(error, match=message):
        create_partitions(
            pd.DataFrame({"id": range(5), "label": list("ABCDE")}), **settings
        )


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
def test_effective_native_calls_and_rounding(layout: str) -> None:
    """Record requested settings and actual native calls independently."""
    three = layout == "train_validation_test"
    parts, record = create_partitions(
        pd.DataFrame({"id": range(5), "label": list("ABCDE")}),
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        seed=42,
        test_size=0.3,
        validation_size=0.2 if three else None,
    )
    assert len(parts["test"]) == 2
    calls = [{"test_size": 0.3, "random_state": 42, "shuffle": True, "stratify": None}]
    if three:
        calls.append(
            {
                "test_size": 0.2 / 0.7,
                "random_state": 42,
                "shuffle": True,
                "stratify": None,
            }
        )
    assert record["settings"] == {
        "seed": 42,
        "test_size": 0.3,
        "validation_size": 0.2 if three else None,
        "shuffle": True,
        "stratify": False,
        "calls": calls,
    }
    assert record["method"] == "seeded"
    assert record["protocol"] is None


@pytest.mark.parametrize(
    ("layout", "size", "stratify", "shuffle", "missing", "stage"),
    [
        ("train_test", 1, False, True, False, "test"),
        ("train_validation_test", 2, False, True, False, "validation"),
        ("train_test", 5, True, True, False, "test"),
        ("train_test", 10, True, True, True, "test"),
        ("train_test", 10, True, False, False, "test"),
    ],
)
def test_native_errors_retain_stage_context(
    layout: str,
    size: int,
    stratify: bool,
    shuffle: bool,
    missing: bool,
    stage: str,
) -> None:
    """Native impossible sizes and stratification errors retain exception type."""
    labels: list[object] = ["A"] * (size - 1) + [None if missing else "B"]
    with pytest.raises(ValueError) as caught:
        create_partitions(
            pd.DataFrame({"id": range(size), "label": labels}),
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            seed=42,
            test_size=0.4,
            validation_size=0.2 if layout == "train_validation_test" else None,
            stratify=stratify,
            shuffle=shuffle,
        )
    assert any(stage in note for note in getattr(caught.value, "__notes__", []))


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
def test_explicit_stratification_preserves_literal_class_counts(layout: str) -> None:
    """Stratification uses aligned targets at each native split."""
    frame = pd.DataFrame({"id": range(20), "label": ["A", "B"] * 10})
    parts, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        seed=42,
        test_size=0.2,
        validation_size=0.2 if layout == "train_validation_test" else None,
        stratify=True,
    )
    expected = {"train": {"A": 8, "B": 8}, "test": {"A": 2, "B": 2}}
    if layout == "train_validation_test":
        expected.update(train={"A": 6, "B": 6}, validation={"A": 2, "B": 2})
    for name, part in parts.items():
        assert part["label"].value_counts().to_dict() == expected[name]
        assert part["label"].tolist() == frame.loc[part.index, "label"].tolist()
    settings = cast(dict[str, object], record["settings"])
    assert all(
        call["stratify"] == "label"
        for call in cast(list[dict[str, object]], settings["calls"])
    )


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
def test_unshuffled_native_order(layout: str) -> None:
    """Disabling shuffle preserves native ordered allocation."""
    parts, record = create_partitions(
        pd.DataFrame({"id": range(5), "label": list("ABCDE")}),
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        seed=42,
        test_size=0.4,
        validation_size=0.2 if layout == "train_validation_test" else None,
        shuffle=False,
    )
    assert record["memberships"] == (
        {"train": [0, 1], "validation": [2], "test": [3, 4]}
        if layout == "train_validation_test"
        else {"train": [0, 1, 2], "test": [3, 4]}
    )
    assert len(parts["test"]) == 2


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
@pytest.mark.parametrize("kind", ["time", "group", "supplied"])
def test_supplied_protocol_and_order(layout: str, kind: str) -> None:
    """Supplied membership keeps original indices, targets and declaration."""
    frame = pd.DataFrame(
        {
            "id": range(1, 7),
            "label": list("ABABAB"),
            "observed_at": pd.date_range("2024-01-01", periods=6),
            "group": ["g1", "g1", "g2", "g2", "g3", "g3"],
        },
        index=range(10, 16),
    )
    before = frame.copy(deep=True)
    members = (
        {"train": [2, 1], "validation": [4, 3], "test": [6, 5]}
        if layout == "train_validation_test"
        else {"train": [4, 3, 2, 1], "test": [6, 5]}
    )
    protocol: dict[str, object] = {"kind": kind, "description": "project declaration"}
    if kind != "supplied":
        protocol["column"] = "observed_at" if kind == "time" else "group"
    parts, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        memberships=members,
        protocol=protocol,
    )
    assert record["memberships"] == members
    assert record["protocol"] == protocol
    assert record["method"] == "supplied"
    assert record["settings"] == {}
    for name, ids in members.items():
        assert parts[name]["id"].tolist() == ids
        assert parts[name]["label"].tolist() == ["ABABAB"[i - 1] for i in ids]
        assert parts[name].index.tolist() == [i + 9 for i in ids]
    if kind == "time":
        ordered = list(parts.values())
        assert all(
            left.observed_at.max() < right.observed_at.min()
            for left, right in zip(ordered[:-1], ordered[1:], strict=True)
        )
    if kind == "group":
        assert all(
            set(left.group).isdisjoint(right.group)
            for i, left in enumerate(parts.values())
            for right in list(parts.values())[i + 1 :]
        )
    pd.testing.assert_frame_equal(frame, before)
    parts["train"].iloc[0, 1] = "changed"
    pd.testing.assert_frame_equal(frame, before)


@pytest.mark.parametrize(
    ("frame", "row_id", "target", "error", "message"),
    [
        ([], "id", "label", TypeError, "DataFrame"),
        (
            pd.DataFrame([[1, 2, 3]], columns=["id", "label", "label"]),
            "id",
            "label",
            ValueError,
            "column",
        ),
        (pd.DataFrame({"id": [1, 2], "": [0, 1]}), "id", "", ValueError, "column"),
        (pd.DataFrame({"id": [1, 2], 1: [0, 1]}), "id", "id", ValueError, "column"),
        (
            pd.DataFrame({"id": [1, 2], "label": [0, 1]}),
            "missing",
            "label",
            ValueError,
            "row_id",
        ),
        (
            pd.DataFrame({"id": [1, 2], "label": [0, 1]}),
            "id",
            "missing",
            ValueError,
            "target",
        ),
        (
            pd.DataFrame({"id": [1, 1], "label": [0, 1]}),
            "id",
            "label",
            ValueError,
            "unique",
        ),
        (
            pd.DataFrame({"id": [1, None], "label": [0, 1]}),
            "id",
            "label",
            ValueError,
            "nonmissing",
        ),
        (
            pd.DataFrame({"id": [True, False], "label": [0, 1]}),
            "id",
            "label",
            TypeError,
            "ID",
        ),
        (
            pd.DataFrame({"id": [1.0, 2.0], "label": [0, 1]}),
            "id",
            "label",
            TypeError,
            "ID",
        ),
        (
            pd.DataFrame({"id": [1, "2"], "label": [0, 1]}),
            "id",
            "label",
            TypeError,
            "ID",
        ),
        (
            pd.DataFrame({"id": [[1], [2]], "label": [0, 1]}),
            "id",
            "label",
            TypeError,
            "ID",
        ),
    ],
)
def test_source_declaration_errors(
    frame: object,
    row_id: str,
    target: str,
    error: type[Exception],
    message: str,
) -> None:
    """Reject ambiguous source columns and unsupported source identities."""
    with pytest.raises(error, match=message):
        create_partitions(
            cast(Any, frame),
            row_id=row_id,
            target=target,
            layout="train_test",
            seed=42,
            test_size=0.4,
        )


@pytest.mark.parametrize(
    ("changes", "error", "message"),
    [
        ({"seed": 42}, ValueError, "supplied"),
        ({"test_size": 0.4}, ValueError, "supplied"),
        ({"validation_size": 0.2}, ValueError, "supplied"),
        ({"shuffle": False}, ValueError, "supplied"),
        ({"stratify": True}, ValueError, "supplied"),
        ({"protocol": []}, TypeError, "protocol"),
        ({"protocol": {}}, ValueError, "kind"),
        ({"protocol": {"kind": "other"}}, ValueError, "kind"),
        ({"protocol": {"kind": "time"}}, ValueError, "column"),
        ({"protocol": {"kind": "group", "column": "missing"}}, ValueError, "column"),
        (
            {"protocol": {"kind": "supplied", "description": 1}},
            TypeError,
            "description",
        ),
        ({"protocol": {"kind": "supplied", "extra": "x"}}, ValueError, "protocol"),
        ({"protocol": {"kind": "supplied", "column": "label"}}, ValueError, "protocol"),
    ],
)
def test_supplied_mode_and_protocol_errors(
    changes: dict[str, object],
    error: type[Exception],
    message: str,
) -> None:
    """Supplied declarations cannot pretend to be seeded generation."""
    settings: dict[str, Any] = {
        "row_id": "id",
        "target": "label",
        "layout": "train_test",
        "memberships": {"train": [1, 2, 3, 4], "test": [5, 6]},
    }
    settings.update(changes)
    with pytest.raises(error, match=message):
        create_partitions(
            pd.DataFrame({"id": range(1, 7), "label": list("ABABAB")}), **settings
        )


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
def test_source_identity_and_record_schema(layout: str) -> None:
    """The record identifies consumed native rows and exact library versions."""
    import hashlib
    from importlib.metadata import version

    frame = pd.DataFrame({"id": range(5), "label": list("ABCDE")})
    frame.attrs["ignored"] = "project metadata"
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        seed=42,
        test_size=0.4,
        validation_size=0.2 if layout == "train_validation_test" else None,
    )
    assert set(record) == {
        "schema_version",
        "layout",
        "row_id",
        "target",
        "source",
        "method",
        "settings",
        "protocol",
        "memberships",
    }
    assert record["schema_version"] == "1.0"
    assert record["row_id"] == "id"
    assert record["target"] == "label"
    unhashed = frame.copy(deep=True)
    unhashed.attrs.clear()
    assert record["source"] == {
        "row_count": 5,
        "schema": [{"name": "id", "dtype": "int64"}, {"name": "label", "dtype": "str"}],
        "sha256": hashlib.sha256(
            unhashed.to_parquet(engine="pyarrow", index=False, compression=None)
        ).hexdigest(),
        "identity_format": "pandas-parquet-v1",
        "versions": {
            name: version(name)
            for name in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
        },
    }


@pytest.mark.parametrize(
    "mutation",
    [
        "repeat",
        "index",
        "attrs",
        "value",
        "target",
        "dtype",
        "rows",
        "columns",
        "category_order",
        "category_levels",
        "timezone",
    ],
)
def test_consumed_frame_identity_sensitivity(mutation: str) -> None:
    """Native identity excludes index/attrs and retains values, order and dtype metadata."""
    frame = pd.DataFrame(
        {
            "id": range(6),
            "label": list("ABABAB"),
            "value": [1, 2, 3, 4, 5, 6],
            "category": pd.Categorical(
                list("ABABAB"), categories=["A", "B", "C"], ordered=True
            ),
            "when": pd.date_range("2024-01-01", periods=6, tz="UTC"),
            "nullable": pd.Series([1, None, 3, 4, 5, 6], dtype="Int64"),
        }
    )

    def identity(data: pd.DataFrame) -> object:
        return create_partitions(
            data,
            row_id="id",
            target="label",
            layout="train_test",
            seed=42,
            test_size=0.4,
        )[1]["source"]

    original = identity(frame)
    changed = frame.copy(deep=True)
    if mutation == "index":
        changed.index = pd.RangeIndex(10, 16)
    elif mutation == "attrs":
        changed.attrs["extra"] = {"a": "b"}
    elif mutation == "value":
        changed.loc[0, "value"] = 99
    elif mutation == "target":
        changed.loc[0, "label"] = "B"
    elif mutation == "dtype":
        changed["value"] = changed["value"].astype("float64")
    elif mutation == "rows":
        changed = changed.iloc[::-1]
    elif mutation == "columns":
        changed = changed[list(reversed(changed.columns))]
    elif mutation == "category_order":
        changed["category"] = changed["category"].cat.reorder_categories(
            ["B", "A", "C"]
        )
    elif mutation == "category_levels":
        changed["category"] = changed["category"].cat.add_categories(["D"])
    elif mutation == "timezone":
        changed["when"] = changed["when"].dt.tz_convert("Europe/London")
    updated = identity(changed)
    assert (updated == original) is (mutation in {"repeat", "index", "attrs"})
    assert identity(frame) == original


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
@pytest.mark.parametrize("seeded", [True, False])
def test_project_json_round_trip_and_supplied_reconstruction(
    tmp_path: Path,
    layout: str,
    seeded: bool,
) -> None:
    """Project JSON retains provenance; selected fields reconstruct current rows."""
    frame = pd.DataFrame({"id": range(1, 7), "label": list("ABABAB")})
    members = (
        {"train": [2, 1], "validation": [4, 3], "test": [6, 5]}
        if layout == "train_validation_test"
        else {"train": [4, 3, 2, 1], "test": [6, 5]}
    )
    settings: dict[str, Any] = (
        {
            "seed": 42,
            "test_size": 0.3,
            "validation_size": 0.2 if layout == "train_validation_test" else None,
        }
        if seeded
        else {"memberships": members}
    )
    parts, record = create_partitions(
        frame, row_id="id", target="label", layout=cast(Any, layout), **settings
    )
    path = tmp_path / "split.json"
    with path.open("x", encoding="utf-8") as stream:
        json.dump(record, stream, allow_nan=False)
    with path.open(encoding="utf-8") as stream:
        saved = json.load(stream)
    assert saved == record
    restored, new_record = create_partitions(
        frame,
        row_id=saved["row_id"],
        target=saved["target"],
        layout=saved["layout"],
        memberships=saved["memberships"],
        protocol=saved["protocol"],
    )
    assert new_record["method"] == "supplied"
    assert new_record["settings"] == {}
    assert new_record["source"] == saved["source"]
    assert new_record["memberships"] == saved["memberships"]
    assert saved["method"] == ("seeded" if seeded else "supplied")
    for name, part in parts.items():
        pd.testing.assert_frame_equal(restored[name], part)
    with pytest.raises(ValueError, match="keys"):
        create_partitions(
            frame,
            row_id=saved["row_id"],
            target=saved["target"],
            layout="train_test"
            if layout == "train_validation_test"
            else "train_validation_test",
            memberships=saved["memberships"],
        )
    frame.loc[0, "label"] = "changed"
    _, changed_record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout=saved["layout"],
        memberships=saved["memberships"],
    )
    assert changed_record["source"] != saved["source"]


@pytest.mark.parametrize(
    "ids", [["a", "b", "c", "d"], [2**63, 2**63 + 1, 2**63 + 2, 2**63 + 3]]
)
def test_supplied_scalar_types_are_lossless_json(ids: list[str] | list[int]) -> None:
    """Strings and large unsigned integers survive JSON without float coercion."""
    frame = pd.DataFrame({"id": ids, "label": [0, 1, 0, 1]})
    members = {"train": [ids[1], ids[0]], "test": [ids[3], ids[2]]}
    _, record = create_partitions(
        frame, row_id="id", target="label", layout="train_test", memberships=members
    )
    assert json.loads(json.dumps(record, allow_nan=False))["memberships"] == members


@pytest.mark.parametrize(
    ("policy", "status", "blocked"),
    [
        ("required", "failed", True),
        ("advisory", "failed", False),
        ("passing", "passed", False),
        ("none", "not_checked", False),
    ],
)
def test_extraction_quality_preparation_composition(
    tmp_path: Path,
    policy: str,
    status: str,
    blocked: bool,
) -> None:
    """Only permitted preparation writes the sentinel and consumes checked rows."""
    from agentic_ml.data_assessment import assess_data
    from agentic_ml.data_quality import DataQualityError, run_validated_step
    from agentic_ml.extraction import extract_data

    root = tmp_path / "project"
    root.mkdir()
    source = root / "source.csv"
    source.write_text("id,label,value\n1,A,1\n2,A,3\n3,B,5\n4,B,7\n5,A,9\n6,B,11\n")
    code = root / "prepare.py"
    code.write_text("# Project-owned extraction and preparation\n")

    def extract(
        sources: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        return sources["data"]

    frame, provenance = extract_data(
        extract,
        project_root=root,
        sources={"data": Path("source.csv")},
        destination=Path("extracted"),
        code_paths=[Path("prepare.py")],
    )
    assert len(frame) == 6
    assert provenance
    sentinel = root / "prepared"

    def prepare(
        data: pd.DataFrame, settings: dict[str, object]
    ) -> tuple[dict[str, object], dict[str, object]]:
        assessment = assess_data(data, target="label")
        parts, record = create_partitions(
            data,
            row_id="id",
            target="label",
            layout="train_test",
            seed=42,
            test_size=0.4,
        )
        sentinel.write_text(json.dumps(record, allow_nan=False))
        assert sorted([*parts["train"].id, *parts["test"].id]) == [1, 2, 3, 4, 5, 6]
        return assessment, record

    rules: list[dict[str, object]] = (
        []
        if policy == "none"
        else [
            {
                "id": "rows",
                "kind": "row_count",
                "min": 6 if policy == "passing" else 7,
                "required": policy != "advisory",
            }
        ]
    )
    if blocked:
        with pytest.raises(DataQualityError) as caught:
            run_validated_step(frame, prepare, rules=rules)
        assert caught.value.report["status"] == status
        assert not sentinel.exists()
    else:
        (assessment, record), quality = run_validated_step(frame, prepare, rules=rules)
        assert quality["status"] == status
        assert quality["blocked"] is False
        assert assessment["row_count"] == 6
        assert assessment["target_balance"] == [
            {"value": "A", "count": 3, "proportion": 0.5},
            {"value": "B", "count": 3, "proportion": 0.5},
        ]
        assert cast(dict[str, object], record["source"])["row_count"] == 6
        assert json.loads(sentinel.read_text()) == record
        assert (
            record["source"]
            == create_partitions(
                frame,
                row_id="id",
                target="label",
                layout="train_test",
                seed=42,
                test_size=0.4,
            )[1]["source"]
        )


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
def test_supplied_record_and_protocol_are_independent(layout: str) -> None:
    """Returned membership and protocol cannot mutate the caller's declarations."""
    members = (
        {"train": [1, 2], "validation": [3, 4], "test": [5, 6]}
        if layout == "train_validation_test"
        else {"train": [1, 2, 3, 4], "test": [5, 6]}
    )
    protocol = {"kind": "supplied", "description": "retained"}
    _, record = create_partitions(
        pd.DataFrame({"id": range(1, 7), "label": list("ABABAB")}),
        row_id="id",
        target="label",
        layout=cast(Any, layout),
        memberships=members,
        protocol=protocol,
    )
    cast(dict[str, list[int]], record["memberships"])["train"].append(99)
    cast(dict[str, object], record["protocol"])["description"] = "changed"
    assert 99 not in members["train"]
    assert protocol["description"] == "retained"


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
@pytest.mark.parametrize("mode", ["seeded", "supplied"])
def test_empty_source_has_contextual_value_error(layout: str, mode: str) -> None:
    """Empty frames cannot satisfy native generation or nonempty supplied coverage."""
    names = (
        ["train", "test"] if layout == "train_test" else ["train", "validation", "test"]
    )
    settings: dict[str, Any] = (
        {"memberships": {name: [i] for i, name in enumerate(names)}}
        if mode == "supplied"
        else {
            "seed": 42,
            "test_size": 0.4,
            "validation_size": 0.2 if layout == "train_validation_test" else None,
        }
    )
    with pytest.raises(ValueError):
        create_partitions(
            pd.DataFrame(
                {
                    "id": pd.Series([], dtype="int64"),
                    "label": pd.Series([], dtype="str"),
                }
            ),
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            **settings,
        )


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("layout", []),
        ("row_id", []),
        ("target", []),
    ],
)
def test_unsupported_argument_types(name: str, value: object) -> None:
    """Wrong argument types fail at the public boundary."""
    settings: dict[str, Any] = {
        "row_id": "id",
        "target": "label",
        "layout": "train_test",
        "seed": 42,
        "test_size": 0.4,
    }
    settings[name] = value
    with pytest.raises(TypeError, match=name):
        create_partitions(
            pd.DataFrame({"id": range(5), "label": list("ABCDE")}), **settings
        )


def test_object_integer_ids_normalize_to_python_json_integers() -> None:
    """Integer scalar normalization does not route through lossy floating point."""
    import numpy as np

    frame = pd.DataFrame(
        {
            "id": pd.Series([np.int64(1), np.int64(2), np.int64(3)], dtype=object),
            "label": list("ABA"),
        }
    )
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships=cast(
            Any,
            {"train": [np.int64(2), np.int64(1)], "test": [np.int64(3)]},
        ),
    )
    assert json.loads(json.dumps(record, allow_nan=False))["memberships"] == {
        "train": [2, 1],
        "test": [3],
    }


def test_native_serialization_failure_is_not_a_record(tmp_path: Path) -> None:
    """Unsupported native Parquet data fails without mutating the frame or cwd."""
    import os

    import pyarrow as pa

    frame = pd.DataFrame(
        {"id": range(5), "label": list("ABCDE"), "value": [1 + 2j] * 5}
    )
    before = frame.copy(deep=True)
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        with pytest.raises(
            (pa.ArrowException, ValueError, TypeError), match="Unsupported|complex"
        ):
            create_partitions(
                frame,
                row_id="id",
                target="label",
                layout="train_test",
                seed=42,
                test_size=0.4,
            )
        assert Path.cwd() == tmp_path
    finally:
        os.chdir(cwd)
    pd.testing.assert_frame_equal(frame, before)


@pytest.mark.parametrize("layout", ["train_test", "train_validation_test"])
@pytest.mark.parametrize(
    "mutation",
    ["missing", "extra", "duplicate", "unknown", "coverage", "empty", "overlap"],
)
def test_loaded_membership_failures_in_both_layouts(layout: str, mutation: str) -> None:
    """Malformed project-loaded memberships fail equally in either layout."""
    members = (
        {"train": [1, 2], "validation": [3, 4], "test": [5, 6]}
        if layout == "train_validation_test"
        else {"train": [1, 2, 3, 4], "test": [5, 6]}
    )
    loaded = json.loads(json.dumps(members))
    if mutation == "missing":
        del loaded["test"]
    elif mutation == "extra":
        loaded["other"] = [7]
    elif mutation == "duplicate":
        loaded["test"] = [5, 5, 6]
    elif mutation == "unknown":
        loaded["test"] = [5, 7]
    elif mutation == "coverage":
        loaded["test"] = [5]
    elif mutation == "empty":
        loaded["test"] = []
    elif mutation == "overlap":
        loaded["test"] = [2, 5, 6]
    with pytest.raises(ValueError):
        create_partitions(
            pd.DataFrame({"id": range(1, 7), "label": list("ABABAB")}),
            row_id="id",
            target="label",
            layout=cast(Any, layout),
            memberships=loaded,
        )
