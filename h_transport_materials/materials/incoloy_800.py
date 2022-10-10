import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


# NOTE: sample No. 1.2 Material 1.4876 (second line of Table 2 in Schmidt's paper)
schmidt_diffusivity = Diffusivity(
    D_0=9.7e-3 * 1e-4,  # NOTE: in Shimada 2020 review, the S_0 factor is wrong
    E_D=c.kJ_per_mol_to_eV(56.4),
    range=(1023, 1223),
    isotope="H",
    source="schmidt_studies_1985",
)

schmidt_permeability_S_0 = 6.34e-8 * htm.avogadro_nb  # according to Shimada 2020
schmidt_permeability_E_S = c.kJ_per_mol_to_eV(56.6)


schmidt_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=schmidt_permeability_S_0 / schmidt_diffusivity.pre_exp,
    E_S=schmidt_permeability_E_S - schmidt_diffusivity.act_energy,
    range=(1023, 1223),
    isotope="H",
    source="schmidt_studies_1985",
)

incoloy_800_diffusivities = [schmidt_diffusivity]

incoloy_800_solubilities = [schmidt_solubility]

for prop in incoloy_800_diffusivities + incoloy_800_solubilities:
    prop.material = "incoloy_800"

diffusivities.properties += incoloy_800_diffusivities
solubilities.properties += incoloy_800_solubilities
