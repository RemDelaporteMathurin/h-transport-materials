import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)

from pathlib import Path
import numpy as np


anderl_recombination = Diffusivity(
    D_0=2.9e-14 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=1.92 * htm.ureg.eV * htm.ureg.particle**-1,
    source="anderl_deuterium_1999",
    isotope="D",
)

# diffusivity
data_diffusivity_serra = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_diffusivity_1998.csv",
    delimiter=",",
    dtype=str,
)
data_diffusivity_serra_h = data_diffusivity_serra[2:, :2].astype(float)
data_diffusivity_serra_d = data_diffusivity_serra[2:, 2:].astype(float)


note_serra_diffusivity_h = (
    "Serra equation doesn't match the experimental points on their graph"
    + "\n Serra gives D_0=5.7e-7 m2/s and E_D = 41220 J/mol \n"
    + "ITER also gives a diffusivity but they adapted it from the wrong equations..."
)
serra_diffusivity_h = Diffusivity(
    data_T=1000 / data_diffusivity_serra_h[:, 0] * htm.ureg.K,
    data_y=data_diffusivity_serra_h[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="serra_hydrogen_1998",
    isotope="H",
    note=note_serra_diffusivity_h,
)

note_serra_diffusivity_d = (
    "Serra equation doesn't match the experimental points on their graph"
    + "\n Serra gives D_0=4.8e-7 m2/s and E_D = 40370 J/mol \n"
    + "ITER also gives a diffusivity but they adapted it from the wrong equations..."
)
serra_diffusivity_d = Diffusivity(
    data_T=1000 / data_diffusivity_serra_d[:, 0] * htm.ureg.K,
    data_y=data_diffusivity_serra_d[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="serra_hydrogen_1998",
    isotope="D",
    note=note_serra_diffusivity_d,
)

# solubility
data_solubility_serra = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_solubility_1998.csv", delimiter=","
)

data_solubility_serra_h = data_solubility_serra[2:, :2]
data_solubility_serra_d = data_solubility_serra[2:, 2:]

serra_solubility_h = Solubility(
    data_T=1000 / data_solubility_serra_h[:, 0] * htm.ureg.K,
    data_y=data_solubility_serra_h[:, 1]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    source="serra_hydrogen_1998",
    isotope="H",
)

serra_solubility_d = Solubility(
    data_T=1000 / data_solubility_serra_d[:, 0] * htm.ureg.K,
    data_y=data_solubility_serra_d[:, 1]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    source="serra_hydrogen_1998",
    isotope="D",
)
# ################# Noh 2016 #############################
nog_diffusivity_cucrzr_t = Diffusivity(
    5.05e-4 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.964 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(573 * htm.ureg.K, 873 * htm.ureg.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

nog_solubility_cucrzr_t_1 = Solubility(
    S_0=7.83e20 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.0715 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(573 * htm.ureg.K, 873 * htm.ureg.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

nog_solubility_cucrzr_t_2 = Solubility(
    S_0=5.42e23 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.4 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(573 * htm.ureg.K, 873 * htm.ureg.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

# ################# Anderl 1999 #############################
anderl_diffusivity_cucrzr_d = Diffusivity(
    D_0=2.0e-2 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=1.2 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(700 * htm.ureg.K, 800 * htm.ureg.K),
    source="anderl_deuterium_1999",
    isotope="D",
)

# ################# Penalva 1999 #############################
penalva_diffusivity_cucrzr_h = Diffusivity(
    3.55e-5 * htm.ureg.m**2 * htm.ureg.s**-1,
    65.5e3 * htm.ureg.J * htm.ureg.mol**-1,
    range=(593 * htm.ureg.K, 773 * htm.ureg.K),
    source="penalva_interaction_2012",
    isotope="D",
)

penalva_solubility_cucrzr_h = Solubility(
    S_0=6.71e-3 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=8.4e3 * htm.ureg.J * htm.ureg.mol**-1,
    range=(593 * htm.ureg.K, 773 * htm.ureg.K),
    source="penalva_interaction_2012",
    isotope="D",
)

anderl_recombination = RecombinationCoeff(
    pre_exp=2.9e-14
    * htm.ureg.meter**4
    * htm.ureg.second**-1
    * htm.ureg.particle**-1,
    act_energy=1.92 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    source="anderl_deuterium_1999",
)


houben_permeability = Permeability(
    pre_exp=6e-6
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.mbar**-0.5,
    act_energy=79 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="houben_comparison_2022",
    isotope="D",
)

properties = [
    serra_diffusivity_h,
    serra_diffusivity_d,
    nog_diffusivity_cucrzr_t,
    anderl_diffusivity_cucrzr_d,
    penalva_diffusivity_cucrzr_h,
    serra_solubility_h,
    serra_solubility_d,
    nog_solubility_cucrzr_t_1,
    nog_solubility_cucrzr_t_2,
    penalva_solubility_cucrzr_h,
    anderl_recombination,
    houben_permeability,
]

for prop in properties:
    prop.material = htm.CUCRZR

htm.database += properties
