import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)
import numpy as np

u = htm.ureg


# https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/yttrium
YTTRIUM_MOLAR_VOLUME = 1.99e-5 * u.m**3 * u.mol**-1

begun_solubility_h = Solubility(
    data_T=u.Quantity([1000, 950, 900, 850, 800, 750, 700], u.degC),
    data_y=[0.321, 0.471, 0.722, 1.13, 1.80, 3.08, 5.44]
    * u.torr**-0.5
    / YTTRIUM_MOLAR_VOLUME,
    isotope="H",
    source="begun_equilibrium_2008",
    note="table I",
)

begun_solubility_d = Solubility(
    data_T=u.Quantity([1000, 950, 900, 850, 800, 750, 700], u.degC),
    data_y=[0.291, 0.428, 0.648, 0.998, 1.60, 2.79, 4.51]
    * u.torr**-0.5
    / YTTRIUM_MOLAR_VOLUME,
    isotope="D",
    source="begun_equilibrium_2008",
    note="table I",
)

begun_solubility_t = Solubility(
    data_T=u.Quantity([1000, 950, 900, 850, 800, 750, 700], u.degC),
    data_y=[0.240, 0.358, 0.545, 0.840, 1.28, 2.13, 3.34]
    * u.torr**-0.5
    / YTTRIUM_MOLAR_VOLUME,
    isotope="T",
    source="begun_equilibrium_2008",
    note="table I",
)

properties = [begun_solubility_h, begun_solubility_d, begun_solubility_t]

for prop in properties:
    prop.material = htm.YTTRIUM

htm.database += properties
