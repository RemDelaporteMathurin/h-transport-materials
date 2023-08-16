import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
    Diffusivity,
    Solubility,
    DissociationCoeff,
    RecombinationCoeff,
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
    range=(673 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 9",
)

tominetti_diffusivity_h = Diffusivity(
    D_0=5.53e-5 * u.m**2 * u.s**-1,
    E_D=84.6 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 8",
)

forcey_solubility_d = Solubility(
    S_0=2.62e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-12.6 * u.kJ * u.mol**-1,
    range=(515 * u.K, 742 * u.K),
    isotope="D",
    source="forcey_permeability_1993",
    note="Equation 10",
)

tominetti_solubility_d = Solubility(
    S_0=3.58e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-16.9 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 13",
)

tominetti_solubility_h = Solubility(
    S_0=6.90e-4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-11.8 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 12",
)

tominetti_dissociation_d = DissociationCoeff(
    pre_exp=0.71e-6 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=75.9 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 16",
)

tominetti_dissociation_h = DissociationCoeff(
    pre_exp=8.81e-8 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=61.2 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 15",
)

tominetti_recombination_d = RecombinationCoeff(
    pre_exp=10.27 * u.m**4 * u.s**-1 * u.mol**-1,
    act_energy=111.6 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="D",
    source="tominetti_solubility_1990",
    note="Equation 16",
)

tominetti_recombination_h = RecombinationCoeff(
    pre_exp=0.26 * u.m**4 * u.s**-1 * u.mol**-1,
    act_energy=87.0 * u.kJ * u.mol**-1,
    range=(673 * u.K, 873 * u.K),
    isotope="H",
    source="tominetti_solubility_1990",
    note="Equation 15",
)

tominetti_permeability_h = tominetti_diffusivity_h * tominetti_solubility_h
tominetti_permeability_h.source = "tominetti_solubility_1990"
tominetti_permeability_h.isotope = "H"
tominetti_permeability_h.range = (673 * u.K, 873 * u.K)

properties = [
    forcey_permeability_d,
    forcey_diffusivity_d,
    tominetti_diffusivity_d,
    tominetti_diffusivity_h,
    forcey_solubility_d,
    tominetti_solubility_d,
    tominetti_solubility_h,
    tominetti_dissociation_d,
    tominetti_dissociation_h,
    tominetti_recombination_d,
    tominetti_recombination_h,
    tominetti_permeability_h,
]

for prop in properties:
    prop.material = htm.TZM

htm.database += properties
