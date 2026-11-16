"""Explicitly authored native features; factories never fit or inspect data."""

from typing import TypedDict

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


class OutputColumn(TypedDict):
    """One project-assigned output name and native dtype."""

    name: str
    dtype: str


class FeatureVariant(TypedDict):
    """An unfitted pipeline with ordered input and output declarations."""

    name: str
    selected_columns: list[str]
    pipeline: Pipeline
    output_schema: list[OutputColumn]


ESTIMATOR_BINDINGS = {"decision_tree": DecisionTreeClassifier}


def mixed_variant(*, scale: bool) -> FeatureVariant:
    """Compose numeric groups with and without scaling and fixed categorical width."""
    steps: list[tuple[str, object]] = [("impute", SimpleImputer(strategy="mean"))]
    if scale:
        steps.append(("scale", StandardScaler()))
    return {
        "name": "mixed_scaled" if scale else "mixed_unscaled",
        "selected_columns": ["n", "count", "category"],
        "pipeline": Pipeline(
            [
                (
                    "columns",
                    ColumnTransformer(
                        [
                            ("numeric", Pipeline(steps), ["n"]),
                            (
                                "counts",
                                SimpleImputer(strategy="most_frequent"),
                                ["count"],
                            ),
                            (
                                "category",
                                Pipeline(
                                    [
                                        (
                                            "impute",
                                            SimpleImputer(strategy="most_frequent"),
                                        ),
                                        (
                                            "encode",
                                            OneHotEncoder(
                                                categories=[["a", "b"]],
                                                handle_unknown="ignore",
                                                sparse_output=False,
                                            ),
                                        ),
                                    ]
                                ),
                                ["category"],
                            ),
                        ],
                        remainder="drop",
                        sparse_threshold=0,
                    ),
                )
            ]
        ),
        "output_schema": [
            {"name": name, "dtype": "float64"}
            for name in ("n_value", "count_value", "is_a", "is_b")
        ],
    }


def get_variants() -> list[FeatureVariant]:
    """Construct fresh named alternatives; settings choose which ones to run."""
    variants: list[FeatureVariant] = [
        {
            "name": name,
            "selected_columns": [column],
            "pipeline": Pipeline(
                [("scale", StandardScaler(with_mean=name != "unchanged"))]
            ),
            "output_schema": [{"name": column, "dtype": "float64"}],
        }
        for name, column in (
            ("reference", "constant"),
            ("signal", "signal"),
            ("unchanged", "constant"),
            ("misleading", "misleading"),
        )
    ]
    return variants + [mixed_variant(scale=True), mixed_variant(scale=False)]
