import numpy as np

import h_transport_materials as htm
from h_transport_materials.property_database.lipb.lipb import (
    atom_density_lipb,
    schumacher_solubility,
)

u = htm.ureg


def test_schumacher_solubility_matches_paper_at_873K():
    """Schumacher & Weiss 1990 (equiatomic Li50Pb50):
    ln(x_H * sqrt(1e5 Pa) / P) = -8.17 + 734 / T, with x_H in at.fr"""
    T = 873 * u.K
    paper_atfr = np.exp(-8.17 + 734 / T.magnitude)  # at.fr / sqrt(bar)

    n = atom_density_lipb(nb_li=50, nb_pb=50).to("mol/m**3").magnitude
    value = schumacher_solubility.value(T).to("particle/m**3/Pa**0.5").magnitude
    atfr = value / 6.02214076e23 / n * np.sqrt(1e5)

    np.testing.assert_allclose(atfr, paper_atfr, rtol=0.02)
