import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c
from pathlib import Path
import numpy as np

serra_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/diffusivity.csv",
    delimiter=",",
    names=True,
)

serra_diffusivity_h = Diffusivity(
    data_T=1000 / serra_diffusivity_data["hydrogenX"],
    data_y=serra_diffusivity_data["hydrogenY"],
    isotope="H",
    source="serra_hydrogen_1998-1",
)

serra_diffusivity_d = Diffusivity(
    data_T=1000 / serra_diffusivity_data["deuteriumX"],
    data_y=serra_diffusivity_data["deuteriumY"],
    isotope="D",
    source="serra_hydrogen_1998-1",
)

serra_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/solubility.csv",
    delimiter=",",
    names=True,
)

serra_solubility_h = Solubility(
    units="m-3 Pa-1/2",
    data_T=1000 / serra_solubility_data["hydrogenX"],
    data_y=serra_solubility_data["hydrogenY"] * htm.avogadro_nb,
    isotope="H",
    source="serra_hydrogen_1998-1",
)

serra_solubility_d = Solubility(
    units="m-3 Pa-1/2",
    data_T=1000 / serra_solubility_data["deuteriumX"],
    data_y=serra_solubility_data["deuteriumY"] * htm.avogadro_nb,
    isotope="D",
    source="serra_hydrogen_1998-1",
)


properties = [
    serra_diffusivity_h,
    serra_diffusivity_d,
    serra_solubility_h,
    serra_solubility_d,
]

for prop in properties:
    prop.material = "pdag"

htm.database += properties
