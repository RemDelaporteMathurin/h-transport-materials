import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
    Diffusivity,
    Solubility,
) 
import numpy as np

u = htm.ureg

forcey_permeability_d = Permeability(
    pre_exp=8.32e-8 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=75.5 * u.kJ * u.mol**-1,
    range=(515 * u.K, 742 * u.K),
    isotope="D",
    source="forcey_permeability_1993",
    note="Equation 8",
)

tominetti_permeability_h = Permeability(
    pre_exp=3.82e-8 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=72.8 * u.kJ * u.mol**-1,
    range=(1000 / 1.5 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 14",
)

forcey_diffusivity_d = Diffusivity(
    D_0=3.18e-4 * u.m**2 * u.s**-1,
    E_D=88.1 * u.kJ * u.mol**-1,
    range=(515 * u.K, 742 * u.K),
    isotope="D",
    source="forcey_permeability_1993",
    note="Equation 9",
)

tominetti_diffusivity_d = Diffusivity(
    D_0=1.96e-4 * u.m**2 * u.s**-1,
    E_D=95.5 * u.kJ * u.mol**-1,
    range=(1000 / 1.5 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 9",
)

tominetti_diffusivity_h = Diffusivity(
    D_0=5.53e-5 * u.m**2 * u.s**-1,
    E_D=84.6 * u.kJ * u.mol**-1,
    range=(1000 / 1.5 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 8",
)

forcey_solubility_d = Solubility(
    S_0=2.62e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=12.6 * u.kJ * u.mol**-1,
    range=(515 * u.K, 742 * u.K),
    isotope="D",
    source="forcey_permeability_1993",
    note="Equation 10",
)

tominetti_solubility_d = Solubility(
    S_0=3.58e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=16.9 * u.kJ * u.mol**-1,
    range=(1000 / 1.5 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 13",
)

tominetti_solubility_h = Solubility(
    S_0=6.90e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=11.8 * u.kJ * u.mol**-1,
    range=(1000 / 1.5 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 12",
)

properties = [
    forcey_permeability_d,
    tominetti_permeability_h,
    forcey_diffusivity_d,
    tominetti_diffusivity_d,
    tominetti_diffusivity_h,
    forcey_solubility_d,
    tominetti_solubility_d,
    tominetti_solubility_h,
]

for prop in properties:
    prop.material = htm.TZM

htm.database += properties