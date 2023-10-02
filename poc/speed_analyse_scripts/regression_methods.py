import numpy as np
from scipy.linalg import lstsq
import statsmodels.api as sm
from scipy.optimize import least_squares

from numpy import array, diag, dot, maximum, empty, repeat, ones, sum
from numpy.linalg import inv


# y = p0*x0 + p1+x1 + ...
def fit_fun(p, x):
    return np.dot(p, x)


def lstsq_method(df_part, output):
    M = df_part['frame'].to_numpy()
    x = df_part['x']
    y = df_part['y']

    M = M[:, np.newaxis] ** [0, 1]
    p_x = lstsq(M, x)[0]
    p_y = lstsq(M, y)[0]

    middle_index = len(df_part) // 2
    middle_frame = df_part.iloc[middle_index]["frame"]
    middle_arg = [1, middle_frame]

    output.append((middle_frame, fit_fun(
        p_x, middle_arg), fit_fun(p_y, middle_arg)))

    # middle_index = len(df_part) - 1
    # middle_frame = df_part.iloc[middle_index]["frame"]
    # middle_arg = [1, middle_frame]

    # output.append((middle_frame, fit_fun(
    #     p_x, middle_arg), fit_fun(p_y, middle_arg)))


def OLS_method(df_part, output):
    M = df_part['frame'].to_numpy()
    x = df_part['x']
    y = df_part['y']

    # [1, x]
    M = sm.add_constant(M)
    x_model = sm.OLS(x, M)
    y_model = sm.OLS(y, M)

    x_res_model = x_model.fit()
    y_res_model = y_model.fit()

    middle_index = len(df_part) // 2
    middle_frame = df_part.iloc[middle_index]["frame"]

    x_res_value = x_res_model.fittedvalues[middle_index]
    y_res_value = y_res_model.fittedvalues[middle_index]

    output.append((middle_frame, x_res_value, y_res_value))


def calc_weights(res_sm):
    y_resid = [abs(resid) for resid in res_sm.resid]
    X_resid = sm.add_constant(res_sm.fittedvalues)

    mod_resid = sm.OLS(y_resid, X_resid)
    res_resid = mod_resid.fit()

    mod_fv = res_resid.fittedvalues
    return 1 / (mod_fv ** 2)


def WLS_method(df_part, output):
    M = df_part['frame'].to_numpy()
    x = df_part['x']
    y = df_part['y']

    # [1, x]
    M = sm.add_constant(M)
    x_res_model = sm.OLS(x, M).fit()
    y_res_model = sm.OLS(y, M).fit()

    x_res_model = sm.WLS(x, M, calc_weights(x_res_model)).fit()
    y_res_model = sm.WLS(y, M, calc_weights(y_res_model)).fit()

    middle_index = len(df_part) // 2
    middle_frame = df_part.iloc[middle_index]["frame"]

    x_res_value = x_res_model.fittedvalues[middle_index]
    y_res_value = y_res_model.fittedvalues[middle_index]

    output.append((middle_frame, x_res_value, y_res_value))


def IRLS(y, X, maxiter, w_init=1, d=0.0001, tolerance=0.001):
    n, p = X.shape
    delta = array(repeat(d, n)).reshape(1, n)
    w = repeat(1, n)
    W = diag(w)
    B = dot(inv(X.T.dot(W).dot(X)),
            (X.T.dot(W).dot(y)))
    for _ in range(maxiter):
        _B = B
        _w = abs(y - X.dot(B)).T
        w = float(1) / maximum(delta, _w)
        W = diag(w[0])
        B = dot(inv(X.T.dot(W).dot(X)),
                (X.T.dot(W).dot(y)))
        tol = sum(abs(B - _B))
        if tol < tolerance:
            return B
    return B


def IRLS_method(df_part, output):
    M = df_part['frame'].to_numpy()
    x = df_part['x']
    y = df_part['y']

    # [1, x]
    M = sm.add_constant(M)
    B_x = IRLS(x, M, 2)
    B_y = IRLS(y, M, 2)

    middle_index = len(df_part) // 2
    middle_frame = df_part.iloc[middle_index]["frame"]

    output.append((middle_frame, fit_fun(
        B_x, middle_frame), fit_fun(B_y, middle_frame)))


def find_weights(x, y):
    def object_function(weights):
        # shape - [N, 1]
        wM_weights = weights.reshape(len(weights), 1)

        # [1, x]
        wx = x * (np.sqrt(wM_weights) ** [0, 1])
        wy = y * np.sqrt(weights)

        resid = lstsq(wx, wy)[1]
        return resid

    w0 = np.random.rand(len(x))
    res = least_squares(object_function, w0, bounds=(0, 1), max_nfev=1)
    return res.x


def WLS_least_squares(df_part, output):
    M = df_part['frame'].to_numpy()
    x = df_part['x'].to_numpy()
    y = df_part['y'].to_numpy()

    # [1, x]
    N = len(M)
    M = M.reshape(N, 1) ** [0, 1]

    # weights = np.random.rand(N)
    # M[:, 1] = M[:, 1] * np.sqrt(weights)
    # x = x * np.sqrt(weights)
    # y = y * np.sqrt(weights)

    weights = find_weights(M, x)
    M[:, 1] = M[:, 1] * np.sqrt(weights)
    x = x * np.sqrt(weights)
    y = y * np.sqrt(weights)

    # OLS
    b_x, resid_x = lstsq(M, x)[:2]
    b_y, resid_y = lstsq(M, y)[:2]
    # print(resid_x)

    middle_index = len(df_part) // 2
    middle_frame = df_part.iloc[middle_index]["frame"]
    middle_arg = [1, middle_frame]

    output.append((middle_frame, fit_fun(b_x, middle_arg), fit_fun(b_y, middle_arg)))
