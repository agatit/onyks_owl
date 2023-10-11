import numpy as np

from stitch.speed.regression.Method import Method
import statsmodels.api as sm


class WlsMethod(Method):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_ols = sm.OLS(np.ones(1), np.ones(1))
        self.model_wls = sm.WLS(np.ones(1), np.ones(1))

        self.model_ols_response = None
        self.model_wls_response = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        M = sm.add_constant(x)

        self.model_ols = sm.OLS(y, M)
        self.model_ols_response = self.model_ols.fit()

        weights = self.calc_weights(self.model_ols_response)
        self.model_wls = sm.WLS(y, M, weights)
        self.model_wls_response = self.model_wls.fit()
        self.params = self.model_wls_response.params

    # def predict(self, x: int) -> float:
    #     return self.model_wls_response.fittedvalues[int(x)]

    def predict(self, x: int) -> float:
        return self.fit_fun(self.params, x)

    @staticmethod
    def calc_weights(res_sm):
        y_resid = [abs(resid) for resid in res_sm.resid]
        X_resid = sm.add_constant(res_sm.fittedvalues)

        mod_resid = sm.OLS(y_resid, X_resid)
        res_resid = mod_resid.fit()

        mod_fv = res_resid.fittedvalues
        weights = 1 / (mod_fv ** 2)

        if np.isinf(weights).any():
            weights[weights == np.inf] = 0

        return weights

    def fit_fun(self, p: list, x: int) -> float:
        _x = np.array(x) ** self.arg_format
        return float(np.dot(p, _x))
