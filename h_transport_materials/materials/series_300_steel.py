import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


# NOTE: best fit for 4 different austenitic steels
perng_diffusivity = ArrheniusProperty(
    pre_exp=2.01e-7,
    act_energy=c.kJ_per_mol_to_eV(49.3),
    range=(373, 623),
    source="perng_effects_1986",
    isotope="H",
)

perng_solubility = Solubility(
    units="m-3 Pa-1/2",
    range=(373, 623),
    pre_exp=2.70e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(6.9),
    isotope="H",
    source="perng_effects_1986",
)

series_300_steel_diffusivities = [perng_diffusivity]

series_300_steel_solubilities = [perng_solubility]

for prop in series_300_steel_diffusivities + series_300_steel_solubilities:
    prop.material = "300_series_steel"

diffusivities.properties += series_300_steel_diffusivities
solubilities.properties += series_300_steel_solubilities
