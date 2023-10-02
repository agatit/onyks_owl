import numpy as np
from scipy.linalg import lstsq

from stitch.speed.regression.Method import Method


class LstsqMethod(Method):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        n = len(x)
        M = x.reshape(n, 1) ** self.arg_format
        self.params = lstsq(M, y)[0]

    def predict(self, x: int) -> float:
        return self.fit_fun(self.params, x)

    # y = p0*x0 + p1+x1 + ...
    def fit_fun(self, p: list, x: int) -> float:
        _x = np.array(x) ** self.arg_format
        return float(np.dot(p, _x))
