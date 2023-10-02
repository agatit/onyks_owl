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

        self.model_wls = sm.WLS(y, M, self.calc_weights(self.model_ols_response))
        self.model_wls_response = self.model_wls.fit()

    def predict(self, x: int) -> float:
        return self.model_wls_response.fittedvalues[int(x)]

    @staticmethod
    def calc_weights(res_sm):
        y_resid = [abs(resid) for resid in res_sm.resid]
        X_resid = sm.add_constant(res_sm.fittedvalues)

        mod_resid = sm.OLS(y_resid, X_resid)
        res_resid = mod_resid.fit()

        mod_fv = res_resid.fittedvalues
        return 1 / (mod_fv ** 2)
