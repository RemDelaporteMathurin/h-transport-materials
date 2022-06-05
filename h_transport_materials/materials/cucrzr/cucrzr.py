from h_transport_materials import k_B, Rg, avogadro_nb, diffusivities, solubilities
from h_transport_materials.materials import Material
from h_transport_materials.property import ArrheniusProperty, Solubility

from pathlib import Path
import numpy as np


anderl_recombination = ArrheniusProperty(
    pre_exp=2.9e-14,
    act_energy=1.92,
    source="anderl_deuterium_1999",
    name="Anderl (1999)",
    isotope="D",
)

# these are the equations given in Serra 1998 but some are wrong (not in agreement with the plotted data)
serra_diffusivity_h_eq = ArrheniusProperty(
    pre_exp=5.7e-7,
    act_energy=41220 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="H Serra (1998)",
    isotope="H",
)
serra_diffusivity_d_eq = ArrheniusProperty(
    pre_exp=4.8e-7,
    act_energy=40370 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="D Serra (1998)",
    isotope="D",
)
serra_diffusivity_T_eq = ArrheniusProperty(
    pre_exp=3.07e-7,
    act_energy=39120 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="T Serra (1998)",
    isotope="T",
)

serra_solubility_h_eq = Solubility(
    pre_exp=0.9 * avogadro_nb,
    act_energy=38580 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="H Serra (1998)",
    isotope="H",
    units="m-3 Pa-1/2",
)
serra_solubility_d_eq = Solubility(
    pre_exp=0.71 * avogadro_nb,
    act_energy=37380 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="D Serra (1998)",
    isotope="D",
    units="m-3 Pa-1/2",
)
serra_solubility_t_eq = Solubility(
    pre_exp=0.84 * avogadro_nb,
    act_energy=38540 * k_B / Rg,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="T Serra (1998)",
    isotope="T",
    units="m-3 Pa-1/2",
)


# these are the fitted values from the experimental points in Serra 1998

# diffusivity
data_diffusivity_serra = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_diffusivity_1998.csv",
    delimiter=",",
    dtype=str,
)
data_diffusivity_serra_h = data_diffusivity_serra[2:, :2].astype(float)
data_diffusivity_serra_d = data_diffusivity_serra[2:, 2:].astype(float)


serra_diffusivity_h = ArrheniusProperty(
    data_T=1000 / data_diffusivity_serra_h[:, 0],
    data_y=data_diffusivity_serra_h[:, 1],
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="H Serra (1998) (refitted)",
    isotope="H",
)

serra_diffusivity_d = ArrheniusProperty(
    data_T=1000 / data_diffusivity_serra_d[:, 0],
    data_y=data_diffusivity_serra_d[:, 1],
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="D Serra (1998) (refitted)",
    isotope="D",
)

# solubility
data_solubility_serra = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_solubility_1998.csv",
    delimiter=",",
    dtype=str,
)
data_solubility_serra_h = data_solubility_serra[2:, :2][:-1].astype(float)
data_solubility_serra_d = data_solubility_serra[2:, 2:].astype(float)

serra_solubility_h = Solubility(
    data_T=1000 / data_solubility_serra_h[:, 0],
    data_y=data_solubility_serra_h[:, 1] * avogadro_nb,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="H Serra (1998) (refitted)",
    isotope="H",
    units="m-3 Pa-1/2",
)

serra_solubility_d = Solubility(
    data_T=1000 / data_solubility_serra_d[:, 0],
    data_y=data_solubility_serra_d[:, 1] * avogadro_nb,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="D Serra (1998) (refitted)",
    isotope="D",
    units="m-3 Pa-1/2",
)

serra_diffusivity_iter = ArrheniusProperty(
    pre_exp=3.92e-7,
    act_energy=0.418,
    range=(553, 773),
    source="serra_hydrogen_1998",
    name="T Serra acc. ITER (1998)",
    isotope="T",
)

cucrzr = Material(D=serra_diffusivity_h, S=serra_solubility_h, name="cucrzr")

# ################# Noh 2016 #############################
nog_diffusivity_cucrzr_t = ArrheniusProperty(
    5.05e-4,
    0.964,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
)

nog_solubility_cucrzr_t_1 = Solubility(
    pre_exp=7.83e20,
    act_energy=0.0715,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
    units="m-3 Pa-1/2",
)

nog_solubility_cucrzr_t_2 = Solubility(
    pre_exp=5.42e23,
    act_energy=0.4,
    range=(573, 873),
    source="noh_hydrogen-isotope_2016",
    name="T Noh (2016)",
    isotope="T",
    units="m-3 Pa-1/2",
)

# ################# Anderl 1999 #############################
anderl_diffusivity_cucrzr_d = ArrheniusProperty(
    pre_exp=2.0e-2,
    act_energy=1.2,
    range=(700, 800),
    source="anderl_deuterium_1999",
    name="D Anderl (1999)",
    isotope="D",
)

# ################# Penalva 1999 #############################
penalva_diffusivity_cucrzr_h = ArrheniusProperty(
    3.55e-5,
    65.5e3 * k_B / Rg,
    range=(593, 773),
    source="penalva_interaction_2012",
    name="D Penalva (1999)",
    isotope="D",
)

penalva_solubility_cucrzr_h = Solubility(
    pre_exp=6.71e-3 * avogadro_nb,
    act_energy=8.4e3 * k_B / Rg,
    range=(593, 773),
    source="penalva_interaction_2012",
    name="D Penalva (1999)",
    isotope="D",
    units="m-3 Pa-1/2",
)

cucrzr_diffusivities = [
    serra_diffusivity_h_eq,
    serra_diffusivity_d_eq,
    serra_diffusivity_T_eq,
    serra_diffusivity_h,
    serra_diffusivity_d,
    serra_diffusivity_iter,
    nog_diffusivity_cucrzr_t,
    anderl_diffusivity_cucrzr_d,
    penalva_diffusivity_cucrzr_h,
]

cucrzr_solubilities = [
    serra_solubility_h_eq,
    serra_solubility_d_eq,
    serra_solubility_t_eq,
    serra_solubility_h,
    serra_solubility_d,
    nog_solubility_cucrzr_t_1,
    nog_solubility_cucrzr_t_2,
    penalva_solubility_cucrzr_h,
]

for prop in cucrzr_diffusivities + cucrzr_solubilities:
    prop.material = "cucrzr"

diffusivities.properties += cucrzr_diffusivities
solubilities.properties += cucrzr_solubilities
