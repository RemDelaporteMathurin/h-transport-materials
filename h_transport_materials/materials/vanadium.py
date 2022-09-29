import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


volk_diffusivity = ArrheniusProperty(
    pre_exp=2.9e-8,
    act_energy=c.kJ_per_mol_to_eV(4.2),
    isotope="H",
    source="volkl_5_1975",
    range=(173, 573),
)

veleckis_solubility = Solubility(
    units="m-3 Pa-1/2",
    isotope="H",
    range=(519, 827),
    pre_exp=1.38e-1 * htm.avogadro_nb,
    act_energy=c / c.kJ_per_mol_to_eV(-29.0),
    source="veleckis_thermodynamic_1969"
)

vanadium_diffusivities = [volk_diffusivity]

vanadium_solubilities = [veleckis_solubility]

for prop in vanadium_diffusivities + vanadium_solubilities:
    prop.material = "vanadium"

diffusivities.properties += vanadium_diffusivities
solubilities.properties += vanadium_solubilities
