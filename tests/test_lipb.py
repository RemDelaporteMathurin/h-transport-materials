import numpy as np
import pytest

import h_transport_materials as htm
from h_transport_materials.property_database.lipb.lipb import (
    molar_mass_lipb,
    rho_lipb,
    schumacher_solubility,
)

u = htm.ureg

# standard atomic weights (g/mol), independent of lipb.py
M_LI = 6.941
M_PB = 207.2


@pytest.mark.parametrize("nb_li,nb_pb", [(17, 83), (50, 50)])
def test_molar_mass_lipb(nb_li, nb_pb):
    """molar mass of LiPb compounds from standard atomic weights"""
    expected = (nb_li * M_LI + nb_pb * M_PB) / 100
    assert molar_mass_lipb(nb_li, nb_pb).to("g/mol").magnitude == pytest.approx(expected)


def test_schumacher_solubility_matches_paper_at_873K():
    """Schumacher & Weiss 1990 (equiatomic Li50Pb50):
    ln(x_H * sqrt(1e5 Pa) / P) = -8.17 + 734 / T, with x_H in at.fr

    The atom density is computed here from the atomic weights rather than
    with atom_density_lipb, so an error in lipb.py doesn't cancel out.
    """
    T = 873 * u.K
    paper_atfr = np.exp(-8.17 + 734 / T.magnitude)  # at.fr / sqrt(bar)

    molar_mass = (0.5 * M_LI + 0.5 * M_PB) * u.g / u.mol
    n = (rho_lipb / molar_mass).to("mol/m**3").magnitude
    value = schumacher_solubility.value(T).to("particle/m**3/Pa**0.5").magnitude
    atfr = value / 6.02214076e23 / n * np.sqrt(1e5)

    np.testing.assert_allclose(atfr, paper_atfr, rtol=0.02)
