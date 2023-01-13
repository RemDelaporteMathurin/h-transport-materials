import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)


webb_permeability = Permeability(
    pre_exp=htm.conversion.ccSTP_to_mol(190)
    * htm.ureg.mol
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.atm**-0.5,
    act_energy=13800 * htm.ureg.cal * htm.ureg.mol**-1,
    isotope="H",
    range=(1 / 0.0015 * htm.ureg.K, 1 / 0.0014 * htm.ureg.K),
    source="webb_permeation_1965",
    note="Table 1",
)

properties = [webb_permeability]

for prop in properties:
    prop.material = "hastelloy_n"

htm.database += properties
