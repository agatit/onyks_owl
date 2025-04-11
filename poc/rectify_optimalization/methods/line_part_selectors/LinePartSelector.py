from abc import ABC, abstractmethod

import numpy as np


class LinePartSelector(ABC):
    @abstractmethod
    def select(self, lines: np.ndarray) -> np.ndarray:
        pass
