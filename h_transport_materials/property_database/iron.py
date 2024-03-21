import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    RecombinationCoeff,
    Permeability,
)

u = htm.ureg

# TODO give units to IRON_MOLAR_VOLUME
# https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/iron
IRON_MOLAR_VOLUME = 7.09e-6  # m3/mol

volkl_diffusivity = Diffusivity(
    D_0=4.00e-8 * u.m**2 * u.s**-1,
    E_D=4.5 * u.kJ * u.mol**-1,
    isotope="H",
    range=(573 * u.K, 1073 * u.K),
    source="volkl_5_1975",
)

tahara_diffusivity_H = Diffusivity(
    D_0=4.43e-8 * u.m**2 * u.s**-1,
    E_D=5.3 * u.kJ * u.mol**-1,
    isotope="H",
    range=(500 * u.K, 1000 * u.K),
    source="tahara_measurements_1985",
)

tahara_diffusivity_D = Diffusivity(
    D_0=4.28e-8 * u.m**2 * u.s**-1,
    E_D=6.47 * u.kJ * u.mol**-1,
    isotope="D",
    range=(500 * u.K, 1000 * u.K),
    source="tahara_measurements_1985",
)

tahara_permeability_h = Permeability(
    pre_exp=1.77e-5 * u.mol * u.m**-1 * u.s**-1 * u.MPa**-0.5,
    act_energy=31.6 * u.kJ * u.mol**-1,
    isotope="H",
    range=(500 * u.K, 1000 * u.K),
    source="tahara_measurements_1985",
    note="equation 4",
)

tahara_permeability_d = Permeability(
    pre_exp=1.05e-5 * u.mol * u.m**-1 * u.s**-1 * u.MPa**-0.5,
    act_energy=32.4 * u.kJ * u.mol**-1,
    isotope="D",
    range=(500 * u.K, 1000 * u.K),
    source="tahara_measurements_1985",
    note="equation 5",
)

eichenauer_solubility = Solubility(
    S_0=4.90e-6 / IRON_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=24.3 * u.kJ * u.mol**-1,
    range=(473 * u.K, 1183 * u.K),
    isotope="H",
    source="eichenauer_diffusion_1958",
)


nagasaki_recombination_alpha = RecombinationCoeff(
    pre_exp=1.26e-17 * u.cm**4 * u.s**-1 * u.particle**-1,
    act_energy=39.2 * u.kJ * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(600, u.degC),
        u.Quantity(900, u.degC),
    ),
    source="nagasaki_ion-driven_1993",
    note="gamma iron, Nagasaki also gives an equivalent form for the recombination coefficient. Here we take the Arrhenius one (Eq. 9)",
)


nagasaki_recombination_gamma = RecombinationCoeff(
    pre_exp=9.93e-20 * u.cm**4 * u.s**-1 * u.particle**-1,
    act_energy=78.8 * u.kJ * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(900, u.degC),
        u.Quantity(1050, u.degC),
    ),
    source="nagasaki_ion-driven_1993",
    note="gamma iron, Nagasaki also gives an equivalent form for the recombination coefficient. Here we take the Arrhenius one (Eq. 9)",
)

# TODO fit this ourselves
addach_diffusivity = Diffusivity(
    D_0=1.02e-6 * u.cm**2 * u.s**-1,
    E_D=19.6 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(25, u.degC),
        u.Quantity(45, u.degC),
    ),
    isotope="H",
    source="addach_hydrogen_2005",
)

masui_permeability_alpha = Permeability(
    pre_exp=113 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.atm**-0.5,
    act_energy=8190 * u.cal * u.mol**-1,
    range=(
        u.Quantity(200, u.degC),
        u.Quantity(850, u.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
    note="alpha phase",
)

masui_permeability_gamma = Permeability(
    pre_exp=1630 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.atm**-0.5,
    act_energy=16900 * u.cal * u.mol**-1,
    range=(
        u.Quantity(930, u.degC),
        u.Quantity(1000, u.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
    note="gamma phase",
)

properties = [
    volkl_diffusivity,
    tahara_diffusivity_H,
    tahara_diffusivity_D,
    tahara_permeability_h,
    tahara_permeability_d,
    eichenauer_solubility,
    nagasaki_recombination_alpha,
    nagasaki_recombination_gamma,
    addach_diffusivity,
    masui_permeability_alpha,
    masui_permeability_gamma,
]

for prop in properties:
    prop.material = htm.IRON

htm.database += properties
