import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

import numpy as np

tanabe_diffusivity = ArrheniusProperty(
    pre_exp=4.00e-8,
    act_energy=c.kJ_per_mol_to_eV(22.3),
    isotope="H",
    range=(500, 1100),
    source="tanabe_hydrogen_1992",
)

katsuta_diffusivity = ArrheniusProperty(
    pre_exp=np.exp(-17.547),
    act_energy=1.266e3 * htm.k_B,
    isotope="H",
    range=(833, 1193),
    source="katsuta_diffusivity_1982",
)

tanabe_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=3.3 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(37.4),
    range=(500, 1100),
    isotope="H",
    source="tanabe_hydrogen_1992",
)

katsuta_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=np.exp(8.703) * htm.avogadro_nb,
    act_energy=7.863e3 * htm.k_B,
    isotope="H",
    source="katsuta_diffusivity_1982",
)

molybdenum_diffusivities = [tanabe_diffusivity, katsuta_diffusivity]

molybdenum_solubilities = [tanabe_solubility, katsuta_solubility]

for prop in molybdenum_diffusivities + molybdenum_solubilities:
    prop.material = "molybdenum"

diffusivities.properties += molybdenum_diffusivities
solubilities.properties += molybdenum_solubilities
