import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability

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

qi_diffusivity_h = Diffusivity(
    D_0=3.1e-4 * u.cm**2 * u.s**-1,
    E_D=0.045 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-130, u.degC),
        u.Quantity(200, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="H",
)

qi_diffusivity_d = Diffusivity(
    D_0=3.8e-4 * u.cm**2 * u.s**-1,
    E_D=0.073 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-130, u.degC),
        u.Quantity(200, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="D",
)

qi_diffusivity_t = Diffusivity(
    D_0=5.6e-4 * u.cm**2 * u.s**-1,
    E_D=0.094 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-130, u.degC),
        u.Quantity(200, u.degC),
    ),
    source="qi_tritium_1983",
    note="table 1, temperature range from Fig 1",
    isotope="T",
)  # TODO get data from experimental points, see issue #64

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
    qi_diffusivity_h,
    qi_diffusivity_d,
    qi_diffusivity_t,
    malo_permeability,
]

for prop in properties:
    prop.material = htm.VANADIUM

htm.database += properties
