import numpy as np
import scipy.stats as stats
from h_transport_materials import k_B
import matplotlib.pyplot as plt


def D(T, D_0, E_D):
    return D_0 * np.exp(-E_D / k_B / T)


def fit_arhenius(D, T):
    D_ln = np.log(D)
    T_inv = 1 / T

    res = stats.linregress(T_inv, D_ln)
    D_0 = np.exp(res.intercept)
    E_D = -res.slope * k_B
    return D_0, E_D


def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None, color=None):
    """Return an axes of confidence bands using a simple approach.
    Notes
    -----
    .. math:: \left| \: \hat{\mu}_{y|x0} - \mu_{y|x0} \: \right| \; \leq \; T_{n-2}^{.975} \; \hat{\sigma} \; \sqrt{\frac{1}{n}+\frac{(x_0-\bar{x})^2}{\sum_{i=1}^n{(x_i-\bar{x})^2}}}
    .. math:: \hat{\sigma} = \sqrt{\sum_{i=1}^n{\frac{(y_i-\hat{y})^2}{n-2}}}
    References
    ----------
    .. [1] M. Duarte.  "Curve fitting," Jupyter Notebook.
       http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/CurveFitting.ipynb
    """
    if ax is None:
        ax = plt.gca()
    y2_log = np.log(y2)
    ci = (
        t
        * s_err
        * np.sqrt(1 / n + (x2 - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
    )
    fill = ax.fill_between(x2, np.exp(y2_log + ci), np.exp(y2_log - ci), alpha=0.2)
    if color is not None:
        fill.set_color(color)
    return ax


def regression_plot(T_exp, D_exp, ci=0.95, color=None):
    D_0, E_D = fit_arhenius(D_exp, T_exp)

    n = D_exp.size  # number of observations
    m = 2  # number of parameters
    dof = n - m  # degrees of freedom
    t = stats.t.ppf(ci, n - m)

    # Estimates of Error in Data/Model
    y_model = D(T_exp, D_0, E_D)
    resid = np.log(D_exp) - np.log(y_model)
    # chi2 = np.sum((resid / np.log(y_model)**2))                        # chi-squared; estimates error in data
    # chi2_red = chi2 / dof                                      # reduced chi-squared; measures goodness of fit
    s_err = np.sqrt(np.sum(resid**2) / dof)
    T_2 = np.linspace(min(T_exp), max(T_exp), endpoint=False)
    D_2 = D(T_2, D_0, E_D)
    (l,) = plt.plot(1 / T_2, D_2)
    if color is not None:
        l.set_color(color)
    plt.scatter(1 / T_exp, D_exp, color=l.get_color())

    plot_ci_manual(t, s_err, n, 1 / T_exp, 1 / T_2, D_2, color=l.get_color())
    return D_0, E_D
