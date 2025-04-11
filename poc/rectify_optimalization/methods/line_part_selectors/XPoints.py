import numpy as np

from rectify_optimalization.methods.line_part_selectors.LinePartSelector import LinePartSelector


class XPoints(LinePartSelector):

    def select(self, lines: np.ndarray) -> np.ndarray:
        return lines[:, :, 0]
