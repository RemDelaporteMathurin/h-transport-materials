import numpy as np
import pytest

import h_transport_materials as htm

u = htm.ureg


def record(record_id):
    (prop,) = [p for p in htm.database if p.record_id == record_id]
    return prop


# Sieverts' constants in mol m-3 Pa-0.5 as printed in Tables 33 (H) and 35 (D)
# of Alberghi's PhD thesis (Politecnico di Torino, 2023)
ALBERGHI_TABLES = [
    ("H", "a", 300, 1.003e-1),
    ("H", "b", 350, 7.138e-2),
    ("H", "c", 400, 7.708e-2),
    ("H", "d", 430, 8.104e-2),
    ("D", "a", 300, 1.108e-1),
    ("D", "b", 350, 1.273e-1),
    ("D", "c", 430, 9.513e-2),
]


@pytest.mark.parametrize("isotope,suffix,T_C,expected", ALBERGHI_TABLES)
def test_alberghi_solubility_matches_table(isotope, suffix, T_C, expected):
    prop = record(f"htm:LiPb-S-{isotope}-alberghi2023-{suffix}")
    assert prop.isotope == isotope
    T = (T_C + 273.15) * u.K
    assert prop.range[0] <= T <= prop.range[1]
    value = prop.value(T).to("mol m**-3 Pa**-0.5").magnitude
    assert value == pytest.approx(expected, rel=1e-6)


def test_alberghi_diffusivity_matches_thesis_fit():
    """D = 4.96e-8 exp(-38860 / R / T) m2/s, 500 to 650 C"""
    prop = record("htm:SS316L-D-H-alberghi2023")
    T = (600 + 273.15) * u.K
    expected = 4.96e-8 * np.exp(-38860 / (8.314462618 * T.magnitude))
    value = prop.value(T).to("m**2 s**-1").magnitude
    assert value == pytest.approx(expected, rel=1e-4)


def test_alberghi_diffusivity_points_are_table_37():
    prop = record("htm:SS316L-D-H-alberghi2023")
    T = prop.data_T.to("degC").magnitude
    y = prop.data_y.to("m**2 s**-1").magnitude
    assert T == pytest.approx([500, 550, 650])
    assert y == pytest.approx([1.12e-10, 1.84e-10, 3.03e-10])


def test_dolan_bulk_diffusivity_is_the_thesis_fit():
    """D = 0.417 exp(-235 kJ/mol / RT) m2/s, fitted to deuterium desorption
    (Eq. 4.3 and Fig. 4.5)"""
    prop = record("htm:C-D-D-dolan2021")
    T = 1200.0
    fit = 0.417 * np.exp(-235e3 / (8.314462618 * T))
    value = prop.value(T * u.K).to("m**2 s**-1").magnitude
    assert prop.isotope == "D"
    assert value == pytest.approx(fit, rel=1e-4)
