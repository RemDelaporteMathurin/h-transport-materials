import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

import numpy as np

tanabe_diffusivity = Diffusivity(
    D_0=4.00e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=22.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(500, 1100),
    source="tanabe_hydrogen_1992",
)

katsuta_diffusivity = Diffusivity(
    D_0=np.exp(-17.547) * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=1.266e3 * htm.k_B * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(833, 1193),
    source="katsuta_diffusivity_1982",
)

tanabe_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=3.3 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=37.4 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500, 1100),
    isotope="H",
    source="tanabe_hydrogen_1992",
)

katsuta_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=np.exp(8.703) * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=7.863e3 * htm.k_B * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    source="katsuta_diffusivity_1982",
)

properties = [
    tanabe_diffusivity,
    katsuta_diffusivity,
    tanabe_solubility,
    katsuta_solubility,
]

for prop in properties:
    prop.material = "molybdenum"

htm.database += properties
