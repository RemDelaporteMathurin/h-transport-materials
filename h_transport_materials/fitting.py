import numpy as np
import scipy.stats as stats
from h_transport_materials import k_B


def fit_arhenius(D, T):
    D_ln = np.log(D.magnitude)
    T_inv = 1 / T.magnitude

    res = stats.linregress(T_inv, D_ln)
    D_0 = np.exp(res.intercept)
    # TODO make this robust
    E_D = -res.slope * k_B.magnitude
    return D_0, E_D
