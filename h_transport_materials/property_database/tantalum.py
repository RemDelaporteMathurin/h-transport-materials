import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

volkl_diffusivity = Diffusivity(
    D_0=4.40e-8 * u.m**2 * u.s**-1,
    E_D=13.5 * u.kJ * u.mol**-1,
    range=(253 * u.K, 573 * u.K),
    isotope="H",
    source="volkl_5_1975",
)

veleckis_solubility = Solubility(
    S_0=1.32e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-33.7 * u.kJ * u.mol**-1,
    isotope="H",
    range=(623 * u.K, 904 * u.K),
    source="veleckis_thermodynamic_1969",
)


qi_diffusivity_h_low_temp = Diffusivity(
    D_0=0.028e-4 * u.cm**2 * u.s**-1,
    E_D=0.042 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-180, u.degC),
        250 * u.K,
    ),
    note="table 1, temperature range from Fig 1",
    source="qi_tritium_1983",
    isotope="H",
)

qi_diffusivity_h_high_temp = Diffusivity(
    D_0=4.2e-4 * u.cm**2 * u.s**-1,
    E_D=0.136 * u.eV * u.particle**-1,
    range=(
        250 * u.K,
        u.Quantity(100, u.degC),
    ),
    note="table 1, temperature range from Fig 1",
    source="qi_tritium_1983",
    isotope="H",
)

qi_diffusivity_d = Diffusivity(
    D_0=3.8e-4 * u.cm**2 * u.s**-1,
    E_D=0.153 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-140, u.degC),
        u.Quantity(100, u.degC),
    ),
    note="table 1, temperature range from Fig 1",
    source="qi_tritium_1983",
    isotope="D",
)

qi_diffusivity_t = Diffusivity(
    D_0=3.7e-4 * u.cm**2 * u.s**-1,
    E_D=0.162 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-140, u.degC),
        u.Quantity(100, u.degC),
    ),
    note="table 1, temperature range from Fig 1",
    source="qi_tritium_1983",
    isotope="T",
)

properties = [
    volkl_diffusivity,
    veleckis_solubility,
    qi_diffusivity_h_low_temp,
    qi_diffusivity_h_high_temp,
    qi_diffusivity_d,
    qi_diffusivity_t,
]

for prop in properties:
    prop.material = htm.TANTALUM

htm.database += properties
