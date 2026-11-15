"""Native dummy estimators used at the public classification boundary."""

from sklearn.base import BaseEstimator

class DummyClassifier(BaseEstimator):
    def __init__(
        self,
        *,
        strategy: str = ...,
        random_state: int | None = ...,
        constant: object = ...,
    ) -> None: ...

class DummyRegressor(BaseEstimator): ...
