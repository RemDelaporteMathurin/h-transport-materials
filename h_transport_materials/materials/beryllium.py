import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

import numpy as np

from h_transport_materials.property import RecombinationCoeff

abramov_diffusivity = Diffusivity(
    D_0=8.0e-9,
    E_D=c.kJ_per_mol_to_eV(35.1),
    range=(620, 775),
    isotope="D",
    source="abramov_deuterium_1990",
)


shapovalov_solubility = Solubility(
    units="m-3 Pa-1/2",
    isotope="H",
    S_0=1.90e-2 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(16.8),
    range=(673, 1473),
    author="shapovalov",
    source="Shapovalov, V.I., Dukel'skii, Y.M., 1988. Izv. Akad. Nauk SSR Met. 5, 201–203",
    year=1988,
    note="couldn't find the original paper so took values from Shimada 2020 review",
)

jones_diffusivity = Diffusivity(
    isotope="T",
    D_0=np.exp(-6.53) * 1e-4,
    E_D=965 * htm.k_B,
    range=(400, 900),
    source="jones_hydrogen_1967",
)

dolan_recombination = RecombinationCoeff(
    pre_exp=1.46e-29,
    act_energy=0.214,
    source="dolan_assessment_1994",
    isotope="H",
    note="Jones also gives a solubility but the units are weird",
)


properties = [
    shapovalov_solubility,
    abramov_diffusivity,
    jones_diffusivity,
    dolan_recombination,
]

for prop in properties:
    prop.material = "beryllium"

htm.database += properties
