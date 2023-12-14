from itertools import tee

import numpy as np

from rectify_optimalization.objective_functions.methods.Method import Method


class DistanceMethod(Method):
    def _calc(self, rectified_lines) -> np.ndarray:
        line_part = self.line_part_selector.select(rectified_lines)
        return self._calc_distance(line_part).std(axis=1)

    @classmethod
    def _calc_distance(cls, array: np.ndarray) -> np.ndarray:
        x = np.apply_along_axis(cls.__pairwise, 1, array)
        return np.abs(x[:, :, 0] - x[:, :, 1])

    @staticmethod
    def __pairwise(iterable):
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = tee(iterable)
        next(b, None)
        return list(zip(a, b))
