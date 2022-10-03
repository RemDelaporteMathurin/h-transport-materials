import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c


TITANIUM_MOLAR_VOLUME = 1.05e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/titanium

reiter_diffusivity = ArrheniusProperty(
    pre_exp=6.9e-7,
    act_energy=c.kJ_per_mol_to_eV(49.1),
    source="reiter_compilation_1996",
    isotope="T",
    range=(873, 1123),
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=1.06e-5 * htm.avogadro_nb / TITANIUM_MOLAR_VOLUME,
    act_energy=c.kJ_per_mol_to_eV(-42.7),
    range=(873, 1123),
    source="reiter_compilation_1996",
)

titanium_diffusivities = [reiter_diffusivity]

titanium_solubilities = [reiter_solubility]

for prop in titanium_diffusivities + titanium_solubilities:
    prop.material = "titanium"

diffusivities.properties += titanium_diffusivities
solubilities.properties += titanium_solubilities
