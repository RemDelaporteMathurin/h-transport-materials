import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)

import numpy as np
from pathlib import Path

BEF2_DENSITY = 1.99 * htm.ureg.g * htm.ureg.cm**-3
LIF_DENSITY = 2.64 * htm.ureg.g * htm.ureg.cm**-3

BEF2_MASS = (
    47.0089884 * htm.ureg.g * htm.ureg.mol**-1
)  # https://www.webqc.org/molecular-weight-of-BeF2.html
LIF_MASS = (
    25.9394 * htm.ureg.g * htm.ureg.mol**-1
)  # https://www.webqc.org/molecular-weight-of-LiF.html


# TODO add experimental points
calderoni_diffusivity = Diffusivity(
    D_0=9.3e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=42e3 * htm.ureg.J * htm.ureg.mol**-1,
    range=(550 + 273.15, 700 + 273.15),
    source="calderoni_measurement_2008",
    isotope="T",
    note="2LiF–BeF_2",
)

calderoni_solubility = Solubility(
    units="m-3 Pa-1",
    S_0=7.9e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    E_S=35 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(550 + 273.15, 700 + 273.15),
    source="calderoni_measurement_2008",
    isotope="T",
    note="2LiF–BeF_2 ; there's a unit inconsistency in the paper",
)


anderl_diffusivity = Diffusivity(
    data_T=np.array([600, 650]) * htm.ureg.degC,
    data_y=[8.0e-10, 3.0e-9] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="anderl_deuteriumtritium_2004",
    isotope="D",
)

anderl_solubility = Solubility(
    units="m-3 Pa-1",
    data_T=np.array([600, 650]) * htm.ureg.degC,
    data_y=[3.1e-4, 1.0e-4] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    source="anderl_deuteriumtritium_2004",
    isotope="D",
)


data_diffusivity_oishi = np.genfromtxt(
    str(Path(__file__).parent) + "/oishi_1989_diffusivity.csv",
    delimiter=",",
    names=True,
)

oishi_diffusivity = Diffusivity(
    data_T=(1 / data_diffusivity_oishi["X"]) * htm.ureg.K,
    data_y=data_diffusivity_oishi["Y"] * htm.ureg.cm**2 * htm.ureg.s**-1,
    source="oishi_tritium_1989",
    isotope="T",
)

lif_fraction = 0.66
flibe_density_field = lif_fraction * LIF_DENSITY + (1 - lif_fraction) * BEF2_DENSITY
flibe_mass_field = lif_fraction * LIF_MASS + (1 - lif_fraction) * BEF2_MASS

data_solubility_field_h = np.array([3.37e-4, 2.16e-4, 1.51e-4]) * htm.ureg.atm**-1
data_solubility_field_h *= flibe_density_field
data_solubility_field_h *= 1 / flibe_mass_field

field_solubility_h = Solubility(
    units="m-3 Pa-1",
    data_T=np.array([500, 600, 700]) * htm.ureg.degC,
    data_y=data_solubility_field_h,
    source="field_solubilities_1967",
    isotope="H",
    note="HF",
)

data_solubility_field_d = np.array([2.96e-4, 1.83e-4, 1.25e-4]) * htm.ureg.atm**-1
data_solubility_field_d *= flibe_density_field
data_solubility_field_d *= 1 / flibe_mass_field

field_solubility_d = Solubility(
    units="m-3 Pa-1",
    data_T=np.array([500, 600, 700]) * htm.ureg.degC,
    data_y=data_solubility_field_d,
    source="field_solubilities_1967",
    isotope="D",
    note="DF",
)

data_maulinauskas_T = np.array([773.0, 873.0, 973.0]) * htm.ureg.K

# see Equation 1 of original paper for conversion from Kc to solubility
data_maulinauskas_k_c_h = [1.13e-3, 3.17e-3, 3.87e-3]  # Kc adimensionnal
data_maulinauskas_sol_h = data_maulinauskas_k_c_h / htm.Rg / data_maulinauskas_T

data_maulinauskas_k_c_d = [1.41e-3, 2.74e-3, 4.26e-3]  # Kc adimensionnal
data_maulinauskas_sol_d = data_maulinauskas_k_c_d / htm.Rg / data_maulinauskas_T

maulinauskas_solubility_h = Solubility(
    units="m-3 Pa-1",
    data_T=data_maulinauskas_T,
    data_y=data_maulinauskas_sol_h,
    isotope="H",
    source="malinauskas_solubilities_1974",
)

maulinauskas_solubility_d = Solubility(
    units="m-3 Pa-1",
    data_T=data_maulinauskas_T,
    data_y=data_maulinauskas_sol_d,
    isotope="D",
    source="malinauskas_solubilities_1974",
)


properties = [
    calderoni_diffusivity,
    calderoni_solubility,
    anderl_diffusivity,
    anderl_solubility,
    oishi_diffusivity,
    field_solubility_h,
    field_solubility_d,
    maulinauskas_solubility_h,
    maulinauskas_solubility_d,
]

for prop in properties:
    prop.material = "flibe"

htm.database += properties