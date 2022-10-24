import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
from pathlib import Path
import numpy as np


# Fig 6 of Young's paper
data_diffusivity_young = np.genfromtxt(
    str(Path(__file__).parent) + "/young_diffusivity.csv",
    delimiter=",",
)

young_diffusivity = Diffusivity(
    data_T=1e3 / data_diffusivity_young[:, 0] * htm.ureg.K,
    data_y=np.exp(data_diffusivity_young[:, 1])
    * htm.ureg.cm**2
    * htm.ureg.s**-1,
    isotope="H",
    source="young_diffusion_1998",
)

ransley_solubility = Solubility(
    isotope="H",
    units="m-3 Pa-1/2",
    S_0=2.32e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=39.7 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(723, 873),
    author="ransley",
    year=1948,
    source="Ransley, C.E., Neufeld, H., 1948. J. Inst. Met. 74, 599–620",
)

properties = [young_diffusivity, ransley_solubility]

for prop in properties:
    prop.material = "aluminium"

htm.database += properties
