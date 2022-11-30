import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)

import numpy as np
from pathlib import Path

# TODO add experimental points
calderoni_diffusivity = Diffusivity(
    D_0=9.3e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=42e3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500 + 273.15, 700 + 273.15),
    source="calderoni_measurement_2008",
    isotope="T",
    note="2LiF–BeF_2",
)

calderoni_solubility = Solubility(
    units="m-3 Pa-1",
    S_0=7.9e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    E_S=35 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500 + 273.15, 700 + 273.15),
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
    # dtype=str,
    names=True,
)

oishi_diffusivity = Diffusivity(
    data_T=(1 / data_diffusivity_oishi["X"]) * htm.ureg.K,
    data_y=data_diffusivity_oishi["Y"] * htm.ureg.cm**2 * htm.ureg.s**-1,
    source="oishi_tritium_1989",
    isotope="T",
)


properties = [
    calderoni_diffusivity,
    calderoni_solubility,
    anderl_diffusivity,
    anderl_solubility,
    oishi_diffusivity,
]

for prop in properties:
    prop.material = "flibe"

htm.database += properties
