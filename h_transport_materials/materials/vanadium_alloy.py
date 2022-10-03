import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


hashizume_diffusivity = ArrheniusProperty(
    pre_exp=7.50e-4
    * 1e-4,  # NOTE: there is a conversion mistake in Shimada 2020 review
    act_energy=0.13,
    range=(373, 573),
    isotope="T",
    source="hashizume_diffusional_2007",
)

klepikov_solubility = Solubility(
    units="m-3 Pa-1/2",
    data_T=[673, 773, 873, 973, 1073],
    data_y=[1.62e20, 9.84e19, 5.65e19, 4.91e19, 2.94e19],  # taken from Table 2
    isotope="H",
    source="klepikov_hydrogen_2000",
)

vanadium_alloy_diffusivities = [hashizume_diffusivity]

vanadium_alloy_solubilities = [klepikov_solubility]

for prop in vanadium_alloy_diffusivities + vanadium_alloy_solubilities:
    prop.material = "v4cr4ti"

diffusivities.properties += vanadium_alloy_diffusivities
solubilities.properties += vanadium_alloy_solubilities
