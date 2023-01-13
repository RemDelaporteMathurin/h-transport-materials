import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
)

u = htm.ureg

# TODO fit this ourselves
grant_permeability = Permeability(
    pre_exp=4.8e-7 * u.mol * u.s**-1 * u.m**-1 * u.Pa**-0.5,
    act_energy=7.99e3 * u.K * htm.k_B,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="uncertainties given in paper",
)

# TODO fit this ourselves
grant_diffusivity = Diffusivity(
    D_0=1.22e-6 * u.m**2 * u.s**-1,
    E_D=6.60e3 * u.K * htm.k_B,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="uncertainties given in paper",
)

grant_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=grant_permeability.pre_exp / grant_diffusivity.pre_exp,
    E_S=grant_permeability.act_energy - grant_diffusivity.act_energy,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="this is not calculated by Grant in the paper.solubility=permeability/diffusivity was done in HTM",
)

grant_dissociation_clean = DissociationCoeff(
    pre_exp=1.13e-2 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=9.32e3 * u.K * htm.k_B,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="ion-beamed cleaned surface. uncertainties given in paper",
)

grant_dissociation_activated = DissociationCoeff(
    pre_exp=1.17e-1 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=12.76e3 * u.K * htm.k_B,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="activated surface. uncertainties given in paper",
)

grant_dissociation_oxidised = DissociationCoeff(
    pre_exp=1.43e-5 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=7.66e3 * u.K * htm.k_B,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="oxidized surface. uncertainties given in paper",
)

properties = [
    grant_permeability,
    grant_diffusivity,
    grant_solubility,
    grant_dissociation_clean,
    grant_dissociation_activated,
    grant_dissociation_oxidised,
]

for prop in properties:
    prop.material = "ss_304"

htm.database += properties
