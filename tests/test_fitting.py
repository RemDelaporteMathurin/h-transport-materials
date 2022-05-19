import numpy as np
import pytest
import h_transport_materials as htm


@pytest.mark.parametrize(
    "D_0,E_D",
    [
        (
            D_0,
            E_D,
        )
        for D_0 in np.logspace(-7, 20, num=6)
        for E_D in np.linspace(0.1, 1.5, num=5)
    ],
)
def test_fit_arhenius(D_0, E_D):
    """Creates noisy data based on known D_0 and E_D coefficients.
    Fits the noisy data with an Arhenius law and compares the
    computed coefficients with the expected ones.
    """
    T = np.linspace(300, 1200)
    D = D_0 * np.exp(-E_D / htm.k_B / T)

    # add noise
    noise = np.random.normal(0, 0.05, D.shape)
    noisy_D = D * 10**noise

    computed_D_0, computed_E_D = htm.fitting.fit_arhenius(noisy_D, T)
    assert computed_D_0 == pytest.approx(D_0, rel=0.3)
    assert computed_E_D == pytest.approx(E_D, rel=0.3)
