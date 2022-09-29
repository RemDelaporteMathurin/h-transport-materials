import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


young_diffusivity = ArrheniusProperty(
    pre_exp=1.75e-8,
    act_energy=c.kJ_per_mol_to_eV(16.2),
    range=(298, 873),
    isotope="H",
    source="young_diffusion_1998",
)

ransley_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=2.32e-2,
    act_energy=c.kJ_per_mol_to_eV(39.7),
    range=(723, 873),
    author="ransley",
    year="1948",
    source="Ransley, C.E., Neufeld, H., 1948. J. Inst. Met. 74, 599–620",
)


aluminium_diffusivities = [young_diffusivity]

aluminium_solubilities = [ransley_solubility]

for prop in aluminium_diffusivities + aluminium_solubilities:
    prop.material = "aluminium"

diffusivities.properties += aluminium_diffusivities
solubilities.properties += aluminium_solubilities
