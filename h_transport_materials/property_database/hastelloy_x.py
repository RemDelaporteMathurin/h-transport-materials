import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
)

u = htm.ureg

kishimoto_diffusivity = Diffusivity(
    D_0=4.9e-3 * u.cm**2 * u.s**-1,
    E_D=0.45 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=41 * u.ccNTP * u.cm**-3 * u.MPa**-0.5,
    E_S=0.22 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=7.2e3 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.MPa**-0.5,
    act_energy=0.67 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)


masui_permeability = Permeability(
    pre_exp=2290 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.atm**-0.5,
    act_energy=16000 * u.cal * u.mol**-1,
    range=(
        u.Quantity(800, u.degC),
        u.Quantity(1000, u.degC),
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
