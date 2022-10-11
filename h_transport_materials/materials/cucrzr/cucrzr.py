from h_transport_materials import k_B, Rg, avogadro_nb
import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, RecombinationCoeff, Solubility

from pathlib import Path
import numpy as np


anderl_recombination = Diffusivity(
    D_0=2.9e-14,
    E_D=1.92,
    source="anderl_deuterium_1999",
    name="Anderl (1999)",
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
    data_T=1000 / data_diffusivity_serra_h[:, 0],
    data_y=data_diffusivity_serra_h[:, 1],
    range=(553, 773),
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
    data_T=1000 / data_diffusivity_serra_d[:, 0],
    data_y=data_diffusivity_serra_d[:, 1],
    range=(553, 773),
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
    data_T=1000 / data_solubility_serra_h[:, 0],
    data_y=data_solubility_serra_h[:, 1] * avogadro_nb,
    range=(553, 773),
    source="serra_hydrogen_1998",
    isotope="H",
    units="m-3 Pa-1/2",
)

serra_solubility_d = Solubility(
    data_T=1000 / data_solubility_serra_d[:, 0],
    data_y=data_solubility_serra_d[:, 1] * avogadro_nb,
    range=(553, 773),
    source="serra_hydrogen_1998",
    isotope="D",
    units="m-3 Pa-1/2",
)
# ################# Noh 2016 #############################
nog_diffusivity_cucrzr_t = Diffusivity(
    5.05e-4,
    0.964,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
)

nog_solubility_cucrzr_t_1 = Solubility(
    S_0=7.83e20,
    E_S=0.0715,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
    units="m-3 Pa-1/2",
)

nog_solubility_cucrzr_t_2 = Solubility(
    S_0=5.42e23,
    E_S=0.4,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
    units="m-3 Pa-1/2",
)

# ################# Anderl 1999 #############################
anderl_diffusivity_cucrzr_d = Diffusivity(
    D_0=2.0e-2,
    E_D=1.2,
    range=(700, 800),
    source="anderl_deuterium_1999",
    name="D Anderl (1999)",
    isotope="D",
)

# ################# Penalva 1999 #############################
penalva_diffusivity_cucrzr_h = Diffusivity(
    3.55e-5,
    65.5e3 * k_B / Rg,
    range=(593, 773),
    source="penalva_interaction_2012",
    name="D Penalva (1999)",
    isotope="D",
)

penalva_solubility_cucrzr_h = Solubility(
    S_0=6.71e-3 * avogadro_nb,
    E_S=8.4e3 * k_B / Rg,
    range=(593, 773),
    source="penalva_interaction_2012",
    name="D Penalva (1999)",
    isotope="D",
    units="m-3 Pa-1/2",
)

anderl_recombination = RecombinationCoeff(
    pre_exp=2.9e-14,
    act_energy=1.92,
    isotope="D",
    source="anderl_deuterium_1999",
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
]

for prop in properties:
    prop.material = "cucrzr"

htm.database += properties
