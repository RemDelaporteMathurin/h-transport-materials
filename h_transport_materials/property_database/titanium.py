import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

TITANIUM_MOLAR_VOLUME = 1.05e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/titanium

reiter_diffusivity = Diffusivity(
    D_0=6.9e-7 * u.m**2 * u.s**-1,
    E_D=49.1 * u.kJ * u.mol**-1,
    source="reiter_compilation_1996",
    isotope="T",
    range=(873 * u.K, 1123 * u.K),
)

reiter_solubility = Solubility(
    S_0=1.06e-5 / TITANIUM_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-42.7 * u.kJ * u.mol**-1,
    range=(873 * u.K, 1123 * u.K),
    isotope="T",
    source="reiter_compilation_1996",
)

wille_diffusivity_1 = Diffusivity(
    D_0=0.9e-2 * u.cm**2 * u.s**-1,
    E_D=12400 * u.cal * u.mol**-1,
    range=(873 * u.K, 1123 * u.K),
    source="wille_hydrogen_1981",
    isotope="H",
    note=(
        "Table 3-1, item a, Commercial Pure Ti, alpha phase. "
        "Range is unknown and not specified in the report, "
        "assuming same as for Reiter 1996. The report cites "
        "another paper from 1958, but don't have access to it."
    ),
)

wille_diffusivity_2 = Diffusivity(
    D_0=0.27e-2 * u.cm**2 * u.s**-1,
    E_D=14200 * u.cal * u.mol**-1,
    range=(873 * u.K, 1123 * u.K),
    source="wille_hydrogen_1981",
    isotope="H",
    note=(
        "Table 3-1, item b, Commercial Pure Ti, alpha phase. "
        "Range is unknown and not specified in the report, "
        "assuming same as for Reiter 1996. The report cites "
        "a master thesis from Schleicher, H but don't have access to it."
    ),
)

wille_diffusivity_3 = Diffusivity(
    D_0=0.06e-2 * u.cm**2 * u.s**-1,
    E_D=14400 * u.cal * u.mol**-1,
    range=(873 * u.K, 1123 * u.K),
    source="wille_hydrogen_1981",
    isotope="H",
    note=(
        "Table 3-1, item d, Commercial Pure Ti, alpha phase. "
        "Range is unknown and not specified in the report, "
        "assuming same as for Reiter 1996. The report cites "
        "another report from Covington 1979, but don't have access to it."
    ),
)


properties = [
    reiter_diffusivity,
    reiter_solubility,
    wille_diffusivity_1,
    wille_diffusivity_2,
    wille_diffusivity_3,
]

for prop in properties:
    prop.material = htm.TITANIUM

htm.database += properties
