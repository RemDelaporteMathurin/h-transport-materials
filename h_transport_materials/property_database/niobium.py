import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

volkl_diffusivity = Diffusivity(
    D_0=5.00e-8 * u.m**2 * u.s**-1,
    E_D=10.2 * u.kJ * u.mol**-1,
    range=(273 * u.K, 773 * u.K),
    source="volkl_5_1975",
    isotope="H",
)

qi_diffusivity_t = Diffusivity(
    D_0=4.4e-4 * u.cm**2 * u.s**-1,
    E_D=0.133 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-140, u.degC),
        u.Quantity(100, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="T",
)

qi_diffusivity_d = Diffusivity(
    D_0=5.2e-4 * u.cm**2 * u.s**-1,
    E_D=0.127 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-140, u.degC),
        u.Quantity(100, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="D",
)

qi_diffusivity_h_high_temp = Diffusivity(
    D_0=5e-4 * u.cm**2 * u.s**-1,
    E_D=0.106 * u.eV * u.particle**-1,
    range=(
        250 * u.K,
        u.Quantity(100, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="H",
)

qi_diffusivity_h_low_temp = Diffusivity(
    D_0=0.9e-4 * u.cm**2 * u.s**-1,
    E_D=0.068 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-160, u.degC),
        250 * u.K,
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="H",
)

veleckis_solubility = Solubility(
    S_0=1.26e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-35.3 * u.kJ * u.mol**-1,
    range=(625 * u.K, 944 * u.K),
    source="veleckis_thermodynamic_1969",
    isotope="H",
)

sherman_diffusivity_h = Diffusivity(
    D_0=4.4e-8 * u.m**2 * u.s**-1,
    E_D=12.8 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(860, u.degC),
        u.Quantity(1120, u.degC),
    ),
    source="sherman_hydrogen_1983",
    note="equation 13, range taken from figure 9",
    isotope="H",
)

sherman_diffusivity_d = Diffusivity(
    D_0=3.1e-8 * u.m**2 * u.s**-1,
    E_D=14.0 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(860, u.degC),
        u.Quantity(1012, u.degC),
    ),
    source="sherman_hydrogen_1983",
    note="equation after 14, range taken from figure 9",
    isotope="D",
)

properties = [
    volkl_diffusivity,
    qi_diffusivity_t,
    qi_diffusivity_d,
    qi_diffusivity_h_low_temp,
    qi_diffusivity_h_high_temp,
    veleckis_solubility,
    sherman_diffusivity_h,
    sherman_diffusivity_d,
]

for prop in properties:
    prop.material = htm.NIOBIUM

htm.database += properties
