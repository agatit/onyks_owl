from typing import Protocol

import numpy as np


class BatchProcessor(Protocol):
    def __call__(self, frame: list[np.ndarray]) -> list[np.ndarray]:
        ...