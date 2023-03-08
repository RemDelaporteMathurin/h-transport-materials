import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

kishimoto_diffusivity = Diffusivity(
    D_0=1.4e-2 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.55 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=17 * htm.ureg.ccNTP * htm.ureg.cm**-3 * htm.ureg.MPa**-0.5,
    E_S=0.12 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=8.1e3
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.MPa**-0.5,
    act_energy=0.67 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

properties = [
    kishimoto_diffusivity,
    kishimoto_solubility,
    kishimoto_permeability,
]

for prop in properties:
    prop.material = htm.NIMONIC_80A

htm.database += properties
