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

properties = [volkl_diffusivity, veleckis_solubility]

for prop in properties:
    prop.material = htm.TANTALUM

htm.database += properties
