import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

katsuta_diffusivity = ArrheniusProperty(
    pre_exp=8.55e-7,
    act_energy=3.62e3 * htm.k_B,
    range=(947, 1123),
    source="katsuta_diffusivity_1979",
    isotope="H",
)


# TODO try and fit this ourself
mclellan_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=2.6e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(56.7),
    range=(967, 1214),
    source="mclellan_solid_1973",
    isotope="H",
)


silver_diffusivities = []

silver_solubilities = []

for prop in silver_diffusivities + silver_solubilities:
    prop.material = "silver"

diffusivities.properties += silver_diffusivities
solubilities.properties += silver_solubilities
