import numpy as np
from scipy.linalg import lstsq


class RegressionModel:
    def __init__(self):
        self.params = [0, 0]
        self.arg_format = [0, 1]

    def fit(self, x, y):
        n = len(x)
        M = x.reshape(n, 1) ** self.arg_format
        self.params = lstsq(M, y)[0]

    def predict(self, x):
        return self.fit_fun(self.params, x)

    # y = p0*x0 + p1+x1 + ...
    def fit_fun(self, p, x):
        _x = np.array(x) * self.arg_format
        return np.dot(p, _x)
