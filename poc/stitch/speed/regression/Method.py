from abc import ABC, abstractmethod

import numpy as np


class Method(ABC):
    def __init__(self, windows_size: int = 25):
        self._window = np.empty((0, 2))
        self._window_size = windows_size

        self.params = [0, 0]
        self.arg_format = [0, 1]  # [0, x]

    @abstractmethod
    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        pass

    @abstractmethod
    def predict(self, x: int) -> float:
        pass
