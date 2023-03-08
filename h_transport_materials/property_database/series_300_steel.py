import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


perng_diffusivity = Diffusivity(
    D_0=2.01e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=49.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(373 * htm.ureg.K, 623 * htm.ureg.K),
    source="perng_effects_1986",
    isotope="H",
    note="best fit for 4 different austenitic steels",
)

perng_solubility = Solubility(
    range=(373 * htm.ureg.K, 623 * htm.ureg.K),
    S_0=2.70e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=6.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    source="perng_effects_1986",
)

properties = [perng_diffusivity, perng_solubility]

for prop in properties:
    prop.material = htm.STEEL_SERIES_300

htm.database += properties
