import random

import numpy as np

from stitch.speed.regression.Method import Method


class MedianMethod(Method):

    def __init__(self, max_change, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_change = max_change
        self.last_result = 0
        self.result = 0

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        last_frame_index = np.unique(x)[-1]
        mask = x == last_frame_index

        self.result = np.median(y[mask])

    def predict(self, x: int) -> float:
        self.last_result = self.result
        return self.result

