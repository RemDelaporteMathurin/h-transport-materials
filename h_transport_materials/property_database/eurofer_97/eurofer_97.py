import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
from pathlib import Path

import numpy as np

u = htm.ureg

esteban_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/esteban_2007/permeability.csv",
    delimiter=",",
)

esteban_permeability_data_y = esteban_permeability_data[:, 1] 

esteban_permeability = Permeability(
    data_T=1000 / esteban_permeability_data[:, 0] * u.K,
    data_y=esteban_permeability_data[:, 1] * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    source="esteban_hydrogen_2007",
    isotope="H",
)