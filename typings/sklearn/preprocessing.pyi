"""Native scaling/encoding constructors used by preprocessing tests."""

from typing import Any

from sklearn.base import BaseEstimator

class StandardScaler(BaseEstimator):
    def __init__(
        self, *, copy: bool = ..., with_mean: bool = ..., with_std: bool = ...
    ) -> None: ...

class OneHotEncoder(BaseEstimator):
    def __init__(
        self,
        *,
        categories: Any = ...,
        drop: Any = ...,
        sparse_output: bool = ...,
        dtype: Any = ...,
        handle_unknown: str = ...,
        min_frequency: Any = ...,
        max_categories: int | None = ...,
        feature_name_combiner: Any = ...,
    ) -> None: ...
