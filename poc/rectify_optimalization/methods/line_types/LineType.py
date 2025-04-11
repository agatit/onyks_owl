from abc import ABC, abstractmethod

import numpy as np


class LineType(ABC):
    @abstractmethod
    def select(self, lines: list) -> np.ndarray:
        pass