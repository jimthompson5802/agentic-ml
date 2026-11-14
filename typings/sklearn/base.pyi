"""Public estimator parameter inspection used by tracking."""

class BaseEstimator:
    def get_params(self, deep: bool = ...) -> dict[str, object]: ...
