import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability

VANADIUM_MOLAR_VOLUME = 8.34e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/vanadium

u = htm.ureg

volk_diffusivity = Diffusivity(
    D_0=2.9e-8 * u.m**2 * u.s**-1,
    E_D=4.2 * u.kJ * u.mol**-1,
    isotope="H",
    source="volkl_5_1975",
    range=(173 * u.K, 573 * u.K),
)

veleckis_solubility = Solubility(
    isotope="H",
    range=(519 * u.K, 827 * u.K),
    S_0=1.38e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-29.0 * u.kJ * u.mol**-1,
    source="veleckis_thermodynamic_1969",
)

schober_diffusivity = Diffusivity(
    D_0=5.6e-8 * u.m**2 * u.s**-1,
    E_D=9.1 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(-150, u.degC),
        u.Quantity(200, u.degC),
    ),
    source="schober_h_1990",
    isotope="H",
    note="found in Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials",
)  # TODO get data from experimental points, see issue #64

reiter_solubility = Solubility(
    S_0=2.1e-6 / VANADIUM_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-32.2 * u.kJ * u.mol**-1,
    source="reiter_compilation_1996",
    isotope="H",
)

malo_permeability = Permeability(
    pre_exp=1.27e-04 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=8667 * u.K * htm.k_B,
    source="malo_experimental_2022",
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(550, u.degC),
    ),
    isotope="D",
)

properties = [
    volk_diffusivity,
    veleckis_solubility,
    schober_diffusivity,
    reiter_solubility,
    malo_permeability,
]

for prop in properties:
    prop.material = htm.VANADIUM

htm.database += properties
