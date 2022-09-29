import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


# TODO fit it ourselves  https://www.degruyter.com/document/doi/10.1515/zna-1962-0415/html
eichenauer_diffusivity = ArrheniusProperty(
    pre_exp=5.60e-8,
    act_energy=c.kJ_per_mol_to_eV(23.6),
    range=(773, 1273),
    source="eichenauer_messung_1962",
)


# NOTE: this was computed from the permeability of Caskey and Derrick and the diffusivity of Eichenauer
shimada_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=7.8e1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(99.4),
    range=(773, 873),
    source="shimada_608_2020",
)

gold_diffusivities = [eichenauer_diffusivity]

gold_solubilities = [shimada_solubility]

for prop in gold_diffusivities + gold_solubilities:
    prop.material = "gold"

diffusivities.properties += gold_diffusivities
solubilities.properties += gold_solubilities
