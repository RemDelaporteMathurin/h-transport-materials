import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
from pathlib import Path

import numpy as np

u = htm.ureg

esteban_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/esteban_2007/permeability.csv",
    delimiter=",",
)

esteban_permeability = Permeability(
    data_T=1000 / esteban_permeability_data[:, 0] * u.K,
    data_y=esteban_permeability_data[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    source="esteban_hydrogen_2007",
    isotope="H",
)

montupet_leblond_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/montupet_leblond_2021/permeability.csv",
    delimiter=",",
)

montupet_leblond_permeability = Permeability(
    data_T=1000 / montupet_leblond_permeability_data[:, 0] * u.K,
    data_y=montupet_leblond_permeability_data[:, 1]
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1,
    range=(473 * u.K, 673 * u.K),
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

montupet_leblond_diffusivity = Diffusivity(
    D_0=2.52e-07 * u.m**2 * u.s**-1,
    E_D=0.16 * u.eV * u.particle**-1,
    range=(473 * u.K, 673 * u.K),
    note="Data given montupet_leblond_permeation_2021 as effective diffusivity",
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

montupet_leblond_solubility = Solubility(
    S_0=1.76e-01 * u.mol * u.m**-1 * u.Pa**-0.5,
    E_S=0.27 * u.eV * u.particle**-1,
    range=(473 * u.K, 673 * u.K),
    note="Data given montupet_leblond_permeation_2021 as effective solubility",
    source="montupet_leblond_permeation_2021",
    isotope="H",
)

properties = [
    esteban_permeability,
    montupet_leblond_permeability,
    montupet_leblond_diffusivity,
    montupet_leblond_solubility,
]

for prop in properties:
    prop.material = htm.EUROFER

htm.database += properties
