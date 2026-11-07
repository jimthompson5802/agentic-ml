"""Project-owned pandas functions copied into independent installed projects."""

from typing import cast

import pandas as pd

PROJECT_ERROR = RuntimeError("project extraction failed")


def extract_people(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Select, filter and merge using explicitly supplied native pandas settings."""
    minimum = settings["minimum_age"]
    columns = settings["columns"]
    key = settings["join_key"]
    assert isinstance(minimum, int)
    assert isinstance(columns, list)
    assert isinstance(key, str)
    assert settings["join_how"] == "left"
    assert settings["join_validate"] == "many_to_one"
    people = frames["people"]
    joined = people.loc[people["age"].ge(minimum)].merge(
        frames["groups"], on=key, how="left", validate="many_to_one"
    )
    selected = joined.loc[:, columns].sort_values("id").reset_index(drop=True)
    # Mutating callback inputs must not change the original settings/report.
    columns.append("callback-only")
    frames["people"]["age"] = 0
    return selected


def invalid_return(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Return an invalid value to exercise the public native-type check."""
    return cast(pd.DataFrame, 42)


def project_failure(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Raise the same project exception object for identity verification."""
    raise PROJECT_ERROR


def native_failure(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Let pandas report an absent project-selected column."""
    return frames["people"].loc[:, ["absent"]]
