import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
)

NI_MOLAR_VOLUME = 6.59e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/nickel
u = htm.ureg

volkl_diffusivity = Diffusivity(
    D_0=6.87e-7 * u.m**2 * u.s**-1,
    E_D=40.5 * u.kJ * u.mol**-1,
    range=(300 * u.K, 1473 * u.K),
    isotope="H",
    source="volkl_5_1975",
)

robertson_diffusivity = Diffusivity(
    D_0=3.72e-7 * u.m**2 * u.s**-1,
    E_D=40.2 * u.kJ * u.mol**-1,
    range=(273 * u.K, 1673 * u.K),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    isotope="H",
    year=1973,
)

louthan_diffusivity_H = Diffusivity(
    D_0=7.0e-7 * u.m**2 * u.s**-1,
    E_D=39.5 * u.kJ * u.mol**-1,
    range=(300 * u.K, 500 * u.K),
    isotope="H",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_D = Diffusivity(
    D_0=7.0e-7 / 2**0.5 * u.m**2 * u.s**-1,
    E_D=39.5 * u.kJ * u.mol**-1,
    range=(300 * u.K, 500 * u.K),
    isotope="D",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_T = Diffusivity(
    D_0=7.0e-7 / 3**0.5 * u.m**2 * u.s**-1,
    E_D=39.5 * u.kJ * u.mol**-1,
    range=(300 * u.K, 500 * u.K),
    isotope="T",
    source="louthan_hydrogen_1975",
)

robertson_solubility = Solubility(
    S_0=5.52e-6 / NI_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=12.5 * u.kJ * u.mol**-1,
    range=(273 * u.K, 1673 * u.K),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    year=1973,
    isotope="H",
)


louthan_solubility = Solubility(
    S_0=5.5e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=15.8 * u.kJ * u.mol**-1,
    range=(300 * u.K, 500 * u.K),
    isotope="H",
    source="louthan_hydrogen_1975",
)

# TODO fit this ourselves
altunoglu_permeability = Permeability(
    pre_exp=3.35e-7 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=54.24 * u.kJ * u.mol**-1,
    range=(373 * u.K, 623 * u.K),
    isotope="H",
    source="altunoglu_permeation_1991",
)

altonoglu_diffusivity = Diffusivity(
    D_0=7.12e-7 * u.m**2 * u.s**-1,
    E_D=40.64 * u.kJ * u.mol**-1,
    range=(373 * u.K, 623 * u.K),
    isotope="H",
    source="altunoglu_permeation_1991",
)

altonoglu_dissociation_coeff = DissociationCoeff(
    pre_exp=1.44e-6 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=29.68 * u.kJ * u.mol**-1,
    range=(373 * u.K, 623 * u.K),
    isotope="H",
    source="altunoglu_permeation_1991",
)

masui_permeability = Permeability(
    pre_exp=1340
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.atm**-0.5,
    act_energy=13000 * htm.ureg.cal * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(300, htm.ureg.degC),
        htm.ureg.Quantity(1000, htm.ureg.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
)

properties = [
    volkl_diffusivity,
    robertson_diffusivity,
    louthan_diffusivity_H,
    louthan_diffusivity_D,
    louthan_diffusivity_T,
    robertson_solubility,
    louthan_solubility,
    altunoglu_permeability,
    altonoglu_diffusivity,
    altonoglu_dissociation_coeff,
    masui_permeability,
]

for prop in properties:
    prop.material = htm.NICKEL

htm.database += properties
