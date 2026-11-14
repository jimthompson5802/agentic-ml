"""Public fitted pipeline feature-name inspection used by tracking."""

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from .base import BaseEstimator

class Pipeline(BaseEstimator):
    def get_feature_names_out(
        self, input_features: Sequence[str] | None = ...
    ) -> NDArray[np.str_]: ...
