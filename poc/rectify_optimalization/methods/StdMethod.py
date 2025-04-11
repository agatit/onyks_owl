import numpy as np

from rectify_optimalization.methods.Method import Method


class StdMethod(Method):
    def _calc(self, rectified_lines) -> np.ndarray:
        return self.line_part_selector.select(rectified_lines).std(axis=1)
