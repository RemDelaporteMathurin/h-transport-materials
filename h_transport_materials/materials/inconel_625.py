import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


gervasini_diffusivity_H = Diffusivity(
    D_0=1.75e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=52.6 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(650, 900),
    source="gervasini_solubility_1984",
)

gervasini_diffusivity_D = Diffusivity(
    D_0=2.39e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=57.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(650, 900),
    source="gervasini_solubility_1984",
)

gervasini_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=2.09e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=10.52 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(650, 900),
    source="gervasini_solubility_1984",
    isotope="H",
    note="the value of the pre-exp factor conversion was taken from Shimada 2020",
)

properties = [gervasini_diffusivity_H, gervasini_diffusivity_D, gervasini_solubility]

for prop in properties:
    prop.material = "inconel_625"

htm.database += properties
