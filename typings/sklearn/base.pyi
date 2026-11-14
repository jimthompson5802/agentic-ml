"""Public estimator settings and native cloning used by preprocessing."""

from typing import Any, TypeVar

class BaseEstimator:
    def get_params(self, deep: bool = ...) -> dict[str, Any]: ...

_Estimator = TypeVar("_Estimator", bound=BaseEstimator)

def clone(estimator: _Estimator, *, safe: bool = ...) -> _Estimator: ...
