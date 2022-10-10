import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

import numpy as np

tanabe_diffusivity = Diffusivity(
    D_0=4.00e-8,
    E_D=c.kJ_per_mol_to_eV(22.3),
    isotope="H",
    range=(500, 1100),
    source="tanabe_hydrogen_1992",
)

katsuta_diffusivity = Diffusivity(
    D_0=np.exp(-17.547),
    E_D=1.266e3 * htm.k_B,
    isotope="H",
    range=(833, 1193),
    source="katsuta_diffusivity_1982",
)

tanabe_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=3.3 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(37.4),
    range=(500, 1100),
    isotope="H",
    source="tanabe_hydrogen_1992",
)

katsuta_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=np.exp(8.703) * htm.avogadro_nb,
    E_S=7.863e3 * htm.k_B,
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
