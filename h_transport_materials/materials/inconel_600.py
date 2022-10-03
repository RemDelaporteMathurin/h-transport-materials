import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

kishimoto_diffusivity = ArrheniusProperty(
    pre_exp=4.90e-7,
    act_energy=0.44,
    isotope="H",
    range=(873, 1173),
    source="kishimoto_hydrogen_1985",
)

# NOTE: the units for the pre_exponential factor in Kishimoto's paper is weird so took the conversion from Shimada 2020
kishimoto_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=1.62e-1 * htm.avogadro_nb,
    act_energy=0.22,
    isotope="H",
    range=(873, 1173),
    source="kishimoto_hydrogen_1985",
)

inconel_600_diffusivities = [kishimoto_diffusivity]

inconel_600_solubilities = [kishimoto_solubility]

for prop in inconel_600_diffusivities + inconel_600_solubilities:
    prop.material = "inconel_600"

diffusivities.properties += inconel_600_diffusivities
solubilities.properties += inconel_600_solubilities
