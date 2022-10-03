import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


causey_diffusivity = ArrheniusProperty(
    pre_exp=0.93e-4,
    act_energy=2.8,
    range=(900, 1473),
    source="causey_interaction_1989",
    isotope="H",
)

# Equation 5 of Atsumi's paper
atsumi_diffusivity = ArrheniusProperty(
    pre_exp=1.69 * 1e-4,
    act_energy=c.kJ_per_mol_to_eV(251),
    range=(500 + 273.15, 900 + 273.15),
    isotope="D",
    source="atsumi_absorption_1988",
)

atsumi_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=1.9e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(-19.2),
    source="atsumi_absorption_1988",
    isotope="H",
)

carbon_diffusivities = [causey_diffusivity, atsumi_diffusivity]

carbon_solubilities = [atsumi_solubility]

for prop in carbon_diffusivities + carbon_solubilities:
    prop.material = "carbon"

diffusivities.properties += carbon_diffusivities
solubilities.properties += carbon_solubilities
