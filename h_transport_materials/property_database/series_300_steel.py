import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

perng_diffusivity = Diffusivity(
    D_0=2.01e-7 * u.m**2 * u.s**-1,
    E_D=49.3 * u.kJ * u.mol**-1,
    range=(373 * u.K, 623 * u.K),
    source="perng_effects_1986",
    isotope="H",
    note="best fit for 4 different austenitic steels",
)

perng_solubility = Solubility(
    range=(373 * u.K, 623 * u.K),
    S_0=2.70e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=6.9 * u.kJ * u.mol**-1,
    isotope="H",
    source="perng_effects_1986",
)

properties = [perng_diffusivity, perng_solubility]

for prop in properties:
    prop.material = htm.STEEL_SERIES_300

htm.database += properties
