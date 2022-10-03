import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c
from pathlib import Path
import numpy as np


# Fig 6 of Young's paper
data_diffusivity_young = np.genfromtxt(
    str(Path(__file__).parent) + "/young_diffusivity.csv",
    delimiter=",",
)

young_diffusivity = ArrheniusProperty(
    data_T=1e3 / data_diffusivity_young[:, 0],
    data_y=np.exp(data_diffusivity_young[:, 1]) * 1e-4,  # cm2 to m2
    isotope="H",
    source="young_diffusion_1998",
)

ransley_solubility = Solubility(
    isotope="H",
    units="m-3 Pa-1/2",
    pre_exp=2.32e-2 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(39.7),
    range=(723, 873),
    author="ransley",
    year=1948,
    source="Ransley, C.E., Neufeld, H., 1948. J. Inst. Met. 74, 599–620",
)


aluminium_diffusivities = [young_diffusivity]

aluminium_solubilities = [ransley_solubility]

for prop in aluminium_diffusivities + aluminium_solubilities:
    prop.material = "aluminium"

diffusivities.properties += aluminium_diffusivities
solubilities.properties += aluminium_solubilities
