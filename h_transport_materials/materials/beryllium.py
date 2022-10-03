import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

import numpy as np

abramov_diffusivity = ArrheniusProperty(
    pre_exp=8.0e-9,
    act_energy=c.kJ_per_mol_to_eV(35.1),
    range=(620, 775),
    isotope="D",
    source="abramov_deuterium_1990",
)


# NOTE: couldn't find the original paper so took values from Shimada 2020 review
shapovalov_solubility = Solubility(
    units="m-3 Pa-1/2",
    isotope="H",
    pre_exp=1.90e-2 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(16.8),
    range=(673, 1473),
    author="shapovalov",
    source="Shapovalov, V.I., Dukel'skii, Y.M., 1988. Izv. Akad. Nauk SSR Met. 5, 201–203",
    year=1988,
)

jones_diffusivity = ArrheniusProperty(
    isotope="T",
    pre_exp=np.exp(-6.53) * 1e-4,
    act_energy=965 * htm.k_B,
    range=(400, 900),
    source="jones_hydrogen_1967",
)

# NOTE: Jones also gives a solubility but the units are weird

beryllium_diffusivities = [abramov_diffusivity, jones_diffusivity]

beryllium_solubilities = [shapovalov_solubility]

for prop in beryllium_diffusivities + beryllium_solubilities:
    prop.material = "beryllium"

diffusivities.properties += beryllium_diffusivities
solubilities.properties += beryllium_solubilities
