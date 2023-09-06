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

# TODO issue #64
qi_diffusivity = Diffusivity(
    D_0=4.4e-8 * u.m**2 * u.s**-1,
    E_D=0.133 * u.eV * u.particle**-1,
    range=(
        u.Quantity(-140, u.degC),
        u.Quantity(100, u.degC),
    ),
    source="qi_tritium_1983",
    isotope="T",
)

veleckis_solubility = Solubility(
    S_0=1.26e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-35.3 * u.kJ * u.mol**-1,
    range=(625 * u.K, 944 * u.K),
    source="veleckis_thermodynamic_1969",
    isotope="H",
)

properties = [
    volkl_diffusivity,
    qi_diffusivity,
    veleckis_solubility,
]

for prop in properties:
    prop.material = htm.NIOBIUM

htm.database += properties
