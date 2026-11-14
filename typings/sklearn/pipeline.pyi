"""Native pipeline public surface used by preprocessing."""

from typing import Any, Self

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
