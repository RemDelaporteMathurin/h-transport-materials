import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)


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

properties = [
    calderoni_diffusivity,
    calderoni_solubility,
]

for prop in properties:
    prop.material = "flibe"

htm.database += properties
