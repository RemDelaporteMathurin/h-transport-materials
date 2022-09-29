import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

PALLADIUM_MOLAR_VOLUME = 8.85e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/palladium

volkl_diffusivity = ArrheniusProperty(
    pre_exp=2.90e-7,
    act_energy=c.kJ_per_mol_to_eV(22.2),
    range=(223, 873),
    source="volkl_5_1975",
    isotope="H",
)


# TODO: try and fit the data ourself https://www.osti.gov/biblio/4413386
favreau_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=4.45e-1 * htm.avogadro_nb / PALLADIUM_MOLAR_VOLUME,
    act_energy=c.kJ_per_mol_to_eV(-8.4),
    source="favreau_solubility_1954",
    isotope="T",
)

palladium_diffusivities = [volkl_diffusivity]

palladium_solubilities = [favreau_solubility]

for prop in palladium_diffusivities + palladium_solubilities:
    prop.material = "palladium"

diffusivities.properties += palladium_diffusivities
solubilities.properties += palladium_solubilities
