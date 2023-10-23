import random
import warnings

import numpy as np

from stitch.speed.regression.Method import Method


class FilterErrorMethod(Method):

    def __init__(self, recurrent: bool, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        self.y = np.zeros(1)
        self.occurred_iterations = 0

        if recurrent:
            self.get_filter_window = self.recurrent_filter
        else:
            self.get_filter_window = self.filter_error

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        self.y = self.get_filter_window(y)

    def predict(self, x: int) -> float:
        return float(np.mean(self.y))

    def recurrent_filter(self, y: np.ndarray):
        last_len = len(y)

        self.occurred_iterations = 0
        while True:
            y = self.filter_error(y)

            current_len = len(y)
            if current_len == last_len:
                break

            last_len = current_len
            self.occurred_iterations += 1
        return y

    @staticmethod
    def filter_error(y: np.ndarray) -> np.ndarray:
        mean = np.mean(y)
        std = np.std(y)
        diff_from_mean = np.abs(y - mean)

        magnitude = 3
        mask = diff_from_mean < std * magnitude

        result = y[mask]
        if len(result) > 0:
            return result
        else:
            return np.zeros_like(y)
