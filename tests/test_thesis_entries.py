import numpy as np
import pytest

import h_transport_materials as htm
from h_transport_materials.property_database.carbon import dolan_diffusivity_tritium
from h_transport_materials.property_database.lipb import lipb
from h_transport_materials.property_database.steel_316L.steel_316L import (
    alberghi_diffusivity,
)

u = htm.ureg

# Sieverts' constants in mol m-3 Pa-0.5 as printed in Tables 33 (H) and 35 (D)
# of Alberghi's PhD thesis (Politecnico di Torino, 2023)
ALBERGHI_TABLES = [
    ("H", 300, 1.003e-1),
    ("H", 350, 7.138e-2),
    ("H", 400, 7.708e-2),
    ("H", 430, 8.104e-2),
    ("D", 300, 1.108e-1),
    ("D", 350, 1.273e-1),
    ("D", 430, 9.513e-2),
]


@pytest.mark.parametrize("isotope,T_C,expected", ALBERGHI_TABLES)
def test_alberghi_solubility_matches_table(isotope, T_C, expected):
    prop = getattr(lipb, f"alberghi_solubility_{isotope.lower()}_{T_C}c")
    assert prop.isotope == isotope
    T = (T_C + 273.15) * u.K
    assert prop.range[0] < T < prop.range[1]
    value = prop.value(T).to("mol m**-3 Pa**-0.5").magnitude
    assert value == pytest.approx(expected, rel=1e-6)


def test_alberghi_diffusivity_matches_thesis_fit():
    """D = 4.96e-8 exp(-38860 / R / T) m2/s, 500 to 650 C"""
    T = (600 + 273.15) * u.K
    expected = 4.96e-8 * np.exp(-38860 / (8.314462618 * T.magnitude))
    value = alberghi_diffusivity.value(T).to("m**2 s**-1").magnitude
    assert value == pytest.approx(expected, rel=1e-4)


def test_dolan_tritium_diffusivity_matches_thesis_fit_at_873K():
    """The single value agrees with D = 0.417 exp(-235 kJ/mol / RT) m2/s
    quoted by the same thesis"""
    T = 873.15
    fit = 0.417 * np.exp(-235e3 / (8.314462618 * T))
    value = dolan_diffusivity_tritium.value(T * u.K).to("m**2 s**-1").magnitude
    assert dolan_diffusivity_tritium.isotope == "T"
    assert value == pytest.approx(fit, rel=0.02)
