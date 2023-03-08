import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

u = htm.ureg

schmidt_diffusivity = Diffusivity(
    D_0=9.7e-3 * u.cm**2 * u.s**-1,
    E_D=56.4 * u.kJ * u.mol**-1,
    range=(1023 * u.K, 1223 * u.K),
    isotope="H",
    source="schmidt_studies_1985",
    note="sample No. 1.2 Material 1.4876 (second line of Table 2 in Schmidt's paper)"
    + "in Shimada 2020 review, the S_0 factor is wrong",
)


schmidt_permeability = Permeability(
    pre_exp=1.8e-3 * u.ccSTP * u.cm**-1 * u.s**-1 * u.bar**-0.5,
    act_energy=56.6 * u.kJ * u.mol**-1,
    isotope="H",
    source="schmidt_studies_1985",
    note="sample No. 1.2 Material 1.4876 (second line of Table 2 in Schmidt's paper)"
    + "in Shimada 2020 review, the S_0 factor is wrong",
)


schmidt_solubility = Solubility(
    S_0=schmidt_permeability.pre_exp / schmidt_diffusivity.pre_exp,
    E_S=schmidt_permeability.act_energy - schmidt_diffusivity.act_energy,
    range=(1023 * u.K, 1223 * u.K),
    isotope="H",
    source="schmidt_studies_1985",
)

# TODO fit this ourselves Fig. 2
esteban_permeability = Permeability(
    pre_exp=3.94e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=55.6 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
)

# TODO fit this ourselves Fig. 3
esteban_diffusivity = Diffusivity(
    D_0=3.87e-7 * u.m**2 * u.s**-1,
    E_D=47.8 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
)

esteban_solubility = Solubility(
    S_0=0.102 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=7.8 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
)

# TODO fit this ourselves Fig. 5
esteban_diss_coeff_non_oxidised = DissociationCoeff(
    pre_exp=2.67e-10 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=40.1 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
    note="non-oxidised surface",
)

# TODO fit this ourselves Fig. 6
esteban_recomb_coeff_non_oxidised = RecombinationCoeff(
    pre_exp=2.58e-8 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=24.5 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
    note="non-oxidised surface",
)

# TODO fit this ourselves Fig. 5
esteban_diss_coeff_oxidised = DissociationCoeff(
    pre_exp=4.14e-6 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=44.3 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
    note="oxidised surface",
)

# TODO fit this ourselves Fig. 6
esteban_recomb_coeff_oxidised = RecombinationCoeff(
    pre_exp=4.00e-4 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=28.6 * u.kJ * u.mol**-1,
    range=(427 * u.K, 780 * u.K),
    isotope="D",
    source="esteban_diffusive_2002",
    note="oxidised surface",
)


masui_permeability = Permeability(
    pre_exp=2440
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.atm**-0.5,
    act_energy=16500 * htm.ureg.cal * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(800, htm.ureg.degC),
        htm.ureg.Quantity(1000, htm.ureg.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
)

properties = [
    schmidt_diffusivity,
    schmidt_permeability,
    schmidt_solubility,
    esteban_permeability,
    esteban_diffusivity,
    esteban_solubility,
    esteban_diss_coeff_non_oxidised,
    esteban_recomb_coeff_non_oxidised,
    esteban_diss_coeff_oxidised,
    esteban_recomb_coeff_oxidised,
    masui_permeability,
]

for prop in properties:
    prop.material = htm.INCOLOY_800

htm.database += properties
