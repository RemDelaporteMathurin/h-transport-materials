import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
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

grant_recombination_clean = RecombinationCoeff(
    pre_exp=grant_dissociation_clean.pre_exp / (grant_solubility.pre_exp**2),
    act_energy=grant_dissociation_clean.act_energy - 2 * grant_solubility.act_energy,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="ion-beamed cleaned surface. not given in paper, calculated in HTM",
)

grant_recombination_activated = RecombinationCoeff(
    pre_exp=grant_dissociation_activated.pre_exp / (grant_solubility.pre_exp**2),
    act_energy=grant_dissociation_activated.act_energy
    - 2 * grant_solubility.act_energy,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="activated surface. not given in paper, calculated in HTM",
)
grant_recombination_oxidised = RecombinationCoeff(
    pre_exp=grant_dissociation_oxidised.pre_exp / (grant_solubility.pre_exp**2),
    act_energy=grant_dissociation_oxidised.act_energy - 2 * grant_solubility.act_energy,
    range=(645 * u.K, 965 * u.K),
    isotope="H",
    source="grant_hydrogen_1987",
    note="oxidized surface. not given in paper, calculated in HTM",
)

# TODO fit this ourselves
braun_diffusivity = Diffusivity(
    D_0=0.18 * u.cm**2 * u.s**-1,
    E_D=14800 * u.J * u.mol**-1,
    range=(u.Quantity(100, u.degC), u.Quantity(600, u.degC)),
    isotope="D",
    source="braun_determination_1980",
    note="Braun doesn't plot the permeability and assumes a solubility from N.L. Hawkins, Report KAPL 863 (1953)",
)

hawkins_solubility = Solubility(
    S_0=2.2e19 * u.particle * u.cm**-3 * u.bar**-0.5,
    E_S=1700 * u.J * u.mol**-1,
    source="N.L. Hawkins, Report KAPL 863 (1953)",
    author="N.L. Hawkins",
    isotope="H",
    year=1953,
    note="Found in Braun 1980 paper but couldn't find the original reference",
)

braun_permeability = Permeability(
    pre_exp=braun_diffusivity.pre_exp * hawkins_solubility.pre_exp,
    act_energy=braun_diffusivity.act_energy + hawkins_solubility.act_energy,
    range=braun_diffusivity.range,
    isotope="D",
    source="braun_determination_1980",
    note="Braun doesn't plot the permeability and assumes a solubility from N.L. Hawkins, Report KAPL 863 (1953)",
)

# TODO fit this ourselves
braun_recombination_coeff = RecombinationCoeff(
    pre_exp=5.4e-19 * u.particle * u.cm**4 * u.particle**-2 * u.s**-1,
    act_energy=15600 * u.J * u.mol**-1,
    range=(u.Quantity(150, u.degC), u.Quantity(400, u.degC)),
    isotope="D",
    source="braun_determination_1980",
)

braun_dissociation_coeff = DissociationCoeff(
    pre_exp=braun_recombination_coeff.pre_exp * hawkins_solubility.pre_exp**2,
    act_energy=braun_recombination_coeff.act_energy + 2 * hawkins_solubility.act_energy,
    range=braun_diffusivity.range,
    isotope="D",
    source="braun_determination_1980",
    note="not given in paper, calculated in HTM using Hawkins solubility, differs from Fuerst 2020 review (Table 5)",
)

properties = [
    grant_permeability,
    grant_diffusivity,
    grant_solubility,
    grant_dissociation_clean,
    grant_dissociation_activated,
    grant_dissociation_oxidised,
    grant_recombination_clean,
    grant_recombination_activated,
    grant_recombination_oxidised,
    braun_diffusivity,
    braun_recombination_coeff,
    braun_dissociation_coeff,
    braun_permeability,
    hawkins_solubility,
]

for prop in properties:
    prop.material = htm.STEEL_304

htm.database += properties
