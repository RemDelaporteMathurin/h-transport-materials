import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, RecombinationCoeff

IRON_MOLAR_VOLUME = 7.09e-6  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/iron

volkl_diffusivity = Diffusivity(
    D_0=4.00e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=4.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(573 * htm.ureg.K, 1073 * htm.ureg.K),
    source="volkl_5_1975",
)

tahara_diffusivity_H = Diffusivity(
    D_0=4.43e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=5.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(500 * htm.ureg.K, 1000 * htm.ureg.K),
    source="tahara_measurements_1985",
)

tahara_diffusivity_D = Diffusivity(
    D_0=4.28e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=6.47 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(500 * htm.ureg.K, 1000 * htm.ureg.K),
    source="tahara_measurements_1985",
)

eichenauer_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.90e-6
    / IRON_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=24.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(473 * htm.ureg.K, 1183 * htm.ureg.K),
    isotope="H",
    source="eichenauer_diffusion_1958",
)


nagasaki_recombination_alpha = RecombinationCoeff(
    pre_exp=1.26e-17 * htm.ureg.cm**4 * htm.ureg.s**-1 * htm.ureg.particle**-1,
    act_energy=39.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(600, htm.ureg.degC),
        htm.ureg.Quantity(900, htm.ureg.degC),
    ),
    source="nagasaki_ion-driven_1993",
    note="gamma iron, Nagasaki also gives an equivalent form for the recombination coefficient. Here we take the Arrhenius one (Eq. 9)",
)


nagasaki_recombination_gamma = RecombinationCoeff(
    pre_exp=9.93e-20 * htm.ureg.cm**4 * htm.ureg.s**-1 * htm.ureg.particle**-1,
    act_energy=78.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(900, htm.ureg.degC),
        htm.ureg.Quantity(1050, htm.ureg.degC),
    ),
    source="nagasaki_ion-driven_1993",
    note="gamma iron, Nagasaki also gives an equivalent form for the recombination coefficient. Here we take the Arrhenius one (Eq. 9)",
)

properties = [
    volkl_diffusivity,
    tahara_diffusivity_H,
    tahara_diffusivity_D,
    eichenauer_solubility,
    nagasaki_recombination_alpha,
    nagasaki_recombination_gamma,
]

for prop in properties:
    prop.material = htm.IRON

htm.database += properties
