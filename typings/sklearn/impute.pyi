"""Native imputer construction used by the public fitting matrix."""

from typing import Any

from sklearn.base import BaseEstimator

class SimpleImputer(BaseEstimator):
    def __init__(
        self,
        *,
        missing_values: Any = ...,
        strategy: str = ...,
        fill_value: Any = ...,
        copy: bool = ...,
        add_indicator: bool = ...,
        keep_empty_features: bool = ...,
    ) -> None: ...
