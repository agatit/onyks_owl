import numpy as np

from rectify_optimalization.methods.line_part_selectors.LinePartSelector import LinePartSelector


class YPoints(LinePartSelector):
    def select(self, lines: np.ndarray) -> np.ndarray:
        return lines[:, :, 1]
