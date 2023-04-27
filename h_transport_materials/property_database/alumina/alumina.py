import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
)
from pathlib import Path
import numpy as np


serra_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_2005/data.csv",
    delimiter=",",
    names=True,
)

serra_permeability = Permeability(
    data_T=1 / serra_data["permx"] * htm.ureg.K,
    data_y=serra_data["permy"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_diffusivity = Diffusivity(
    data_T=1 / serra_data["diffx"] * htm.ureg.K,
    data_y=serra_data["diffy"] * htm.ureg.m**2 * htm.ureg.s**-1,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_solubility = Solubility(
    data_T=1 / serra_data["solx"] * htm.ureg.K,
    data_y=serra_data["soly"] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)


properties = [
    serra_permeability,
    serra_diffusivity,
    serra_solubility,
]

for prop in properties:
    prop.material = htm.ALUMINA

htm.database += properties
