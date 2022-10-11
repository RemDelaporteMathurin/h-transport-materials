import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


hashizume_diffusivity = Diffusivity(
    D_0=7.50e-4 * 1e-4,
    E_D=0.13,
    range=(373, 573),
    isotope="T",
    source="hashizume_diffusional_2007",
    note="there is a conversion mistake for D_0 in Shimada 2020 review",
)

klepikov_solubility = Solubility(
    units="m-3 Pa-1/2",
    data_T=[673.0, 773.0, 873.0, 973.0, 1073.0],
    data_y=[1.62e20, 9.84e19, 5.65e19, 4.91e19, 2.94e19],
    isotope="H",
    source="klepikov_hydrogen_2000",
    note="taken from Table 2",
)

vanadium_alloy_diffusivities = []

vanadium_alloy_solubilities = []

properties = [hashizume_diffusivity, klepikov_solubility]

for prop in properties:
    prop.material = "v4cr4ti"

htm.database += properties
