"""Public native classification metric used by the project training example."""

def accuracy_score(
    y_true: object,
    y_pred: object,
    *,
    normalize: bool = ...,
    sample_weight: object | None = ...,
) -> float: ...
