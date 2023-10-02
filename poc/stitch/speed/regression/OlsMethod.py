import numpy as np

from stitch.speed.regression.Method import Method
import statsmodels.api as sm


class OlsMethod(Method):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = sm.OLS(np.ones(1), np.ones(1))
        self._response = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        M = sm.add_constant(x)
        self._model = sm.OLS(y, M)
        self._response = self._model.fit()

    def predict(self, x: int) -> float:
        return self._response.fittedvalues[int(x)]
