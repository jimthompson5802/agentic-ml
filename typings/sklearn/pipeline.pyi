"""Native pipeline public surface used by preprocessing."""

from collections.abc import Sequence
from typing import Any, Self

import numpy as np
from numpy.typing import NDArray
from sklearn.base import BaseEstimator

class Pipeline(BaseEstimator):
    def __init__(
        self,
        steps: list[tuple[str, Any]],
        *,
        transform_input: list[str] | None = ...,
        memory: Any = ...,
        verbose: bool = ...,
    ) -> None: ...
    def set_output(self, *, transform: str | None = ...) -> Self: ...
    def fit(self, x: Any, /, y: Any = ..., **params: Any) -> Self: ...
    def transform(self, x: Any, /, **params: Any) -> Any: ...
    def __getitem__(self, ind: Any) -> Any: ...
    def get_feature_names_out(
        self, input_features: Sequence[str] | None = ...
    ) -> NDArray[np.str_]: ...
