import random

import numpy as np

from stitch.speed.regression.Method import Method


class MeanMethod(Method):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_result = 0
        self.result = 0

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        last_frame_index = np.unique(x)[-1]
        mask = x == last_frame_index

        self.result = y[mask].mean()

    def predict(self, x: int) -> float:
        self.last_result = self.result
        return self.result
