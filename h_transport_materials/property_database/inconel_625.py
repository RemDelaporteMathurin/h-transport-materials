import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    DissociationCoeff,
    RecombinationCoeff,
)

u = htm.ureg

gervasini_diffusivity_H = Diffusivity(
    D_0=1.75e-6 * u.m**2 * u.s**-1,
    E_D=52.6 * u.kJ * u.mol**-1,
    isotope="H",
    range=(650 * u.K, 900 * u.K),
    source="gervasini_solubility_1984",
)

gervasini_diffusivity_D = Diffusivity(
    D_0=2.39e-6 * u.m**2 * u.s**-1,
    E_D=57.2 * u.kJ * u.mol**-1,
    isotope="D",
    range=(650 * u.K, 900 * u.K),
    source="gervasini_solubility_1984",
)

gervasini_solubility = Solubility(
    S_0=2.09e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=10.52 * u.kJ * u.mol**-1,
    range=(650 * u.K, 900 * u.K),
    source="gervasini_solubility_1984",
    isotope="H",
    note="the value of the pre-exp factor conversion was taken from Shimada 2020",
)

perujo_dissociation_coeff_clean = DissociationCoeff(
    pre_exp=1.6e-3 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=48.2 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

perujo_recombination_coeff_clean = RecombinationCoeff(
    pre_exp=2.0e-3 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=11.5 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

perujo_dissociation_coeff_oxidised = DissociationCoeff(
    pre_exp=0.26 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=111.3 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="oxidised surface, stationary",
)

perujo_recombination_coeff_oxidised = RecombinationCoeff(
    pre_exp=32.0 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=97.0 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="oxidised surface, stationary",
)

properties = [
    gervasini_diffusivity_H,
    gervasini_diffusivity_D,
    gervasini_solubility,
    perujo_dissociation_coeff_clean,
    perujo_recombination_coeff_clean,
    perujo_dissociation_coeff_oxidised,
    perujo_recombination_coeff_oxidised,
]

for prop in properties:
    prop.material = htm.INCONEL_625

htm.database += properties
