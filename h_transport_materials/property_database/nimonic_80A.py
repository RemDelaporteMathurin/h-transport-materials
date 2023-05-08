import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
)

u = htm.ureg

kishimoto_diffusivity = Diffusivity(
    D_0=1.4e-2 * u.cm**2 * u.s**-1,
    E_D=0.55 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=17 * u.ccNTP * u.cm**-3 * u.MPa**-0.5,
    E_S=0.12 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=8.1e3 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.MPa**-0.5,
    act_energy=0.67 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
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
