import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    DissociationCoeff,
    RecombinationCoeff,
)


gervasini_diffusivity_H = Diffusivity(
    D_0=1.75e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=52.6 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(650 * htm.ureg.K, 900 * htm.ureg.K),
    source="gervasini_solubility_1984",
)

gervasini_diffusivity_D = Diffusivity(
    D_0=2.39e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=57.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(650 * htm.ureg.K, 900 * htm.ureg.K),
    source="gervasini_solubility_1984",
)

gervasini_solubility = Solubility(
    S_0=2.09e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=10.52 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(650 * htm.ureg.K, 900 * htm.ureg.K),
    source="gervasini_solubility_1984",
    isotope="H",
    note="the value of the pre-exp factor conversion was taken from Shimada 2020",
)

perujo_dissociation_coeff_clean = DissociationCoeff(
    pre_exp=1.6e-3
    * htm.ureg.mol
    * htm.ureg.m**-2
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1,
    act_energy=48.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="T",
    range=(450 * htm.ureg.K, 620 * htm.ureg.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

perujo_recombination_coeff_clean = RecombinationCoeff(
    pre_exp=2.0e-3 * htm.ureg.mol**-1 * htm.ureg.m**4 * htm.ureg.s**-1,
    act_energy=11.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="T",
    range=(450 * htm.ureg.K, 620 * htm.ureg.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

perujo_dissociation_coeff_oxidised = DissociationCoeff(
    pre_exp=0.26
    * htm.ureg.mol
    * htm.ureg.m**-2
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1,
    act_energy=111.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="T",
    range=(450 * htm.ureg.K, 620 * htm.ureg.K),
    source="perujo_low_1996",
    note="oxidised surface, stationary",
)

perujo_recombination_coeff_oxidised = RecombinationCoeff(
    pre_exp=32.0 * htm.ureg.mol**-1 * htm.ureg.m**4 * htm.ureg.s**-1,
    act_energy=97.0 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="T",
    range=(450 * htm.ureg.K, 620 * htm.ureg.K),
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
