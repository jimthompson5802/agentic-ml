"""Run with: uv run --locked python examples/assessment_and_splits.py."""

import json

import pandas as pd

from agentic_ml.data_assessment import assess_data
from agentic_ml.splitting import create_partitions


def main() -> None:
    """Display assessment, seeded/supplied splits and membership validation."""
    frame = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "value": [1, 3, 5, None, 9, 11],
            "label": ["A", "A", "B", "B", "A", "B"],
        }
    )
    print("INPUT DATA\n", frame.to_string(index=False), sep="")
    print("\nASSESSMENT (missingness, distributions, target balance)")
    print(json.dumps(assess_data(frame, target="label"), indent=2, allow_nan=False))

    for three_way in (False, True):
        parts, record = create_partitions(
            frame,
            row_id="id",
            target="label",
            layout="train_validation_test" if three_way else "train_test",
            seed=42,
            test_size=0.4,
            validation_size=0.2 if three_way else None,
        )
        print(f"\nSEEDED {record['layout']}")
        for name, part in parts.items():
            print(f"{name}:\n{part.to_string(index=False)}")
        print("Record:", json.dumps(record, indent=2, allow_nan=False))

        # Project code owns JSON save/load; use an in-memory round-trip here.
        saved = json.loads(json.dumps(record, allow_nan=False))
        restored, current = create_partitions(
            frame,
            row_id=saved["row_id"],
            target=saved["target"],
            layout=saved["layout"],
            memberships=saved["memberships"],
        )
        assert all(restored[name].equals(part) for name, part in parts.items())
        print("Reconstructed from JSON:", current["memberships"])
        print("Source identity unchanged:", current["source"] == record["source"])

    print("\nEXPECTED REJECTION: overlapping membership")
    try:
        create_partitions(
            frame,
            row_id="id",
            target="label",
            layout="train_test",
            memberships={"train": [1, 2, 3, 4], "test": [4, 5, 6]},
        )
    except ValueError as error:
        print(error)
    else:
        raise AssertionError("Overlapping membership should have been rejected")


if __name__ == "__main__":
    main()
