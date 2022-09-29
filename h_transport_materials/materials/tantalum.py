import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


volkl_diffusivity = ArrheniusProperty(
    pre_exp=4.40e-8,
    act_energy=c.kJ_per_mol_to_eV(13.5),
    range=(253, 573),
    isotope="H",
    source="volkl_5_1975",
)

veleckis_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=1.32e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(-33.7),
    isotope="H",
    range=(623, 904),
    source="veleckis_thermodynamic_1969",
)

tantalum_diffusivities = [volkl_diffusivity]

tantalum_solubilities = [veleckis_solubility]

for prop in tantalum_diffusivities + tantalum_solubilities:
    prop.material = "tantalum"

diffusivities.properties += tantalum_diffusivities
solubilities.properties += tantalum_solubilities
