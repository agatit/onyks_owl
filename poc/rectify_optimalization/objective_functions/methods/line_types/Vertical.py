import numpy as np

from rectify_optimalization.objective_functions.methods.line_types.LineType import LineType


class Vertical(LineType):
    def select(self, lines: list) -> np.ndarray:
        return np.array(lines[1]["lines"], dtype=np.float64)
