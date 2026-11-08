"""Public train_test_split signature for scikit-learn 1.9."""

from typing import TypeVar

import numpy as np

_Array = TypeVar("_Array")

def train_test_split(
    *arrays: _Array,
    test_size: float | int | None = ...,
    train_size: float | int | None = ...,
    random_state: int | np.random.RandomState | None = ...,
    shuffle: bool = ...,
    stratify: object | None = ...,
) -> list[_Array]: ...
