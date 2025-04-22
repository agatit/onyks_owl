from typing import Protocol

import numpy as np


class FrameProcessor(Protocol):
    def __call__(self, frame: np.ndarray) -> np.ndarray:
        ...