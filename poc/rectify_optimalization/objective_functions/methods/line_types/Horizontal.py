import numpy as np

from rectify_optimalization.objective_functions.methods.line_types.LineType import LineType


class Horizontal(LineType):
    #todo: lines[0]["lines"] na obiekt
    def select(self, lines: list) -> np.ndarray:
        return np.array(lines[0]["lines"], dtype=np.float64)
