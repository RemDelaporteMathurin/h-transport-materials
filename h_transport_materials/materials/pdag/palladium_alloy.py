import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
from pathlib import Path
import numpy as np

serra_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/diffusivity.csv",
    delimiter=",",
    names=True,
)

serra_diffusivity_h = Diffusivity(
    data_T=1000 / serra_diffusivity_data["hydrogenX"] * htm.ureg.K,
    data_y=serra_diffusivity_data["hydrogenY"] * htm.ureg.m**2 * htm.ureg.s**-1,
    isotope="H",
    source="serra_hydrogen_1998-1",
)

serra_diffusivity_d = Diffusivity(
    data_T=1000 / serra_diffusivity_data["deuteriumX"] * htm.ureg.K,
    data_y=serra_diffusivity_data["deuteriumY"] * htm.ureg.m**2 * htm.ureg.s**-1,
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
    data_T=1000 / serra_solubility_data["hydrogenX"] * htm.ureg.K,
    data_y=serra_solubility_data["hydrogenY"]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_1998-1",
)

serra_solubility_d = Solubility(
    units="m-3 Pa-1/2",
    data_T=1000 / serra_solubility_data["deuteriumX"] * htm.ureg.K,
    data_y=serra_solubility_data["deuteriumY"]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
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
