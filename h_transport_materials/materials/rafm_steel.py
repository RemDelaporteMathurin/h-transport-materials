import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


# NOTE: value obtained from a average estimate from several authors
causey_diffusivity = ArrheniusProperty(
    pre_exp=1.00e-7,
    act_energy=c.kJ_per_mol_to_eV(13.2),
    range=(300, 973),
    source="causey_416_2012",
    isotope="H",
)

# NOTE: value obtained from a average estimate from several authors
causey_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=4.40e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(28.6),
    range=(300, 973),
    isotope="H",
    source="causey_416_2012",
)


rafm_steel_diffusivities = [causey_diffusivity]

rafm_steel_solubilities = [causey_solubility]

for prop in rafm_steel_diffusivities + rafm_steel_solubilities:
    prop.material = "rafm_steel"

diffusivities.properties += rafm_steel_diffusivities
solubilities.properties += rafm_steel_solubilities
