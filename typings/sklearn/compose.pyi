"""Native column composition constructor used by preprocessing tests."""

from typing import Any

from sklearn.base import BaseEstimator

class ColumnTransformer(BaseEstimator):
    def __init__(
        self,
        transformers: list[tuple[str, Any, Any]],
        *,
        remainder: Any = ...,
        sparse_threshold: float = ...,
        n_jobs: int | None = ...,
        transformer_weights: Any = ...,
        verbose: bool = ...,
        verbose_feature_names_out: Any = ...,
    ) -> None: ...
