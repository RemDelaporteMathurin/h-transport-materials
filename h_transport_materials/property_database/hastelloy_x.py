import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

kishimoto_diffusivity = Diffusivity(
    D_0=4.9e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.45 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=41 * htm.ureg.ccNTP * htm.ureg.cm**-3 * htm.ureg.MPa**-0.5,
    E_S=0.22 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=7.2e3
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


masui_permeability = Permeability(
    pre_exp=2290
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.atm**-0.5,
    act_energy=16000 * htm.ureg.cal * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(800, htm.ureg.degC),
        htm.ureg.Quantity(1000, htm.ureg.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
)

properties = [
    kishimoto_diffusivity,
    kishimoto_solubility,
    kishimoto_permeability,
    masui_permeability,
]

for prop in properties:
    prop.material = htm.HASTELLOY_X

htm.database += properties
