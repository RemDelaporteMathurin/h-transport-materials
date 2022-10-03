import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c
from h_transport_materials.materials.iron import IRON_MOLAR_VOLUME


# NOTE: this is an average of 10 papers on diffusivity from Reiter compilation review
reiter_diffusivity = ArrheniusProperty(
    pre_exp=3.70e-7,
    act_energy=c.kJ_per_mol_to_eV(51.9),
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
)

# NOTE: this is an average of 5 papers on diffusivity from Reiter compilation review
reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=5.8e-6 * htm.avogadro_nb / IRON_MOLAR_VOLUME,
    act_energy=c.kJ_per_mol_to_eV(13.1),
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
)


steel_316L_diffusivities = [reiter_diffusivity]

steel_316L_solubilities = [reiter_solubility]

for prop in steel_316L_diffusivities + steel_316L_solubilities:
    prop.material = "steel_316l"

diffusivities.properties += steel_316L_diffusivities
solubilities.properties += steel_316L_solubilities
