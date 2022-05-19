from h_transport_materials import k_B, Rg, avogadro_nb, diffusivities, solubilities
from h_transport_materials.materials import Material
from h_transport_materials.property import ArheniusProperty

import numpy as np


anderl_src = "R. A. Anderl et al. 'Deuterium transport in Cu, CuCrZr, and Cu/Be'. In: Journal of Nuclear Materials 266-269 (Mar. 1999), pp. 761–765"
anderl_recombination = ArheniusProperty(
    pre_exp=2.9e-14,
    act_energy=1.92,
    source=anderl_src,
    name="Anderl (1999)",
    year=1999,
    author="anderl",
    isotope="D",
)

serra_src = "E Serra and A Perujo. 'Hydrogen and deuterium transport and inventory parameters in a Cu–0.65Cr–0.08Zr alloy for fusion reactor applications'. en. In: Journal of Nuclear Materials 258-263 (Oct. 1998), pp. 1028–1032"

# these are the equations given in Serra 1998 but some are wrong (not in agreement with the plotted data)
serra_diffusivity_h_eq = ArheniusProperty(
    pre_exp=5.7e-7,
    act_energy=41220 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="H Serra (1998)",
    author="serra",
    isotope="H",
    year=1998,
)
serra_diffusivity_d_eq = ArheniusProperty(
    pre_exp=4.8e-7,
    act_energy=40370 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="D Serra (1998)",
    author="serra",
    isotope="D",
    year=1998,
)
serra_diffusivity_T_eq = ArheniusProperty(
    pre_exp=3.07e-7,
    act_energy=39120 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="T Serra (1998)",
    author="serra",
    isotope="T",
    year=1998,
)

serra_solubility_h_eq = ArheniusProperty(
    pre_exp=0.9 * avogadro_nb,
    act_energy=38580 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="H Serra (1998)",
    author="serra",
    isotope="H",
    year=1998,
)
serra_solubility_d_eq = ArheniusProperty(
    pre_exp=0.71 * avogadro_nb,
    act_energy=37380 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="D Serra (1998)",
    author="serra",
    isotope="D",
    year=1998,
)
serra_solubility_t_eq = ArheniusProperty(
    pre_exp=0.84 * avogadro_nb,
    act_energy=38540 * k_B / Rg,
    range=(553, 773),
    source=serra_src,
    name="T Serra (1998)",
    author="serra",
    isotope="T",
    year=1998,
)


# these are the fitted values from the experimental points in Serra 1998

# diffusivity
data_diffusivity_serra = np.genfromtxt(
    "h_transport_materials/materials/cucrzr/serra_diffusivity_1998.csv",
    delimiter=",",
    dtype=str,
)
data_diffusivity_serra_h = data_diffusivity_serra[2:, :2].astype(float)
data_diffusivity_serra_d = data_diffusivity_serra[2:, 2:].astype(float)


serra_diffusivity_h = ArheniusProperty(
    data_T=1000 / data_diffusivity_serra_h[:, 0],
    data_y=data_diffusivity_serra_h[:, 1],
    range=(553, 773),
    source=serra_src,
    name="H Serra (1998) (refitted)",
    author="serra",
    isotope="H",
    year=1998,
)

serra_diffusivity_d = ArheniusProperty(
    data_T=1000 / data_diffusivity_serra_d[:, 0],
    data_y=data_diffusivity_serra_d[:, 1],
    range=(553, 773),
    source=serra_src,
    name="D Serra (1998) (refitted)",
    author="serra",
    isotope="D",
    year=1998,
)

# solubility
data_solubility_serra = np.genfromtxt(
    "h_transport_materials/materials/cucrzr/serra_solubility_1998.csv",
    delimiter=",",
    dtype=str,
)
data_solubility_serra_h = data_solubility_serra[2:, :2][:-1].astype(float)
data_solubility_serra_d = data_solubility_serra[2:, 2:].astype(float)

serra_solubility_h = ArheniusProperty(
    data_T=1000 / data_solubility_serra_h[:, 0],
    data_y=data_solubility_serra_h[:, 1] * avogadro_nb,
    range=(553, 773),
    source=serra_src,
    name="H Serra (1998) (refitted)",
    author="serra",
    isotope="H",
    year=1998,
)

serra_solubility_d = ArheniusProperty(
    data_T=1000 / data_solubility_serra_d[:, 0],
    data_y=data_solubility_serra_d[:, 1] * avogadro_nb,
    range=(553, 773),
    source=serra_src,
    name="D Serra (1998) (refitted)",
    author="serra",
    isotope="D",
    year=1998,
)

serra_diffusivity_iter = ArheniusProperty(
    pre_exp=3.92e-7,
    act_energy=0.418,
    range=(553, 773),
    source=serra_src,
    author="serra",
    name="T Serra acc. ITER (1998)",
    isotope="T",
    year=1998,
)

cucrzr = Material(D=serra_diffusivity_h, S=serra_solubility_h, name="cucrzr")

# ################# Noh 2016 #############################
nog_diffusivity_cucrzr_t = ArheniusProperty(
    5.05e-4,
    0.964,
    range=(573, 873),
    source="Hydrogen-isotope transport in an ELBRODUR G CuCrZr alloy for nuclear applications in heat sinks, Journal of Nuclear Materials, Volume 473, May 2016, Pages 112–118",
    name="T Noh (2016)",
    author="noh",
    isotope="T",
    year=2016,
)

nog_solubility_cucrzr_t_1 = ArheniusProperty(
    7.83e20,
    0.0715,
    range=(573, 873),
    source="Hydrogen-isotope transport in an ELBRODUR G CuCrZr alloy for nuclear applications in heat sinks, Journal of Nuclear Materials, Volume 473, May 2016, Pages 112–118",
    name="T Noh (2016)",
    author="noh",
    isotope="T",
    year=2016,
)

nog_solubility_cucrzr_t_2 = ArheniusProperty(
    5.42e23,
    0.4,
    range=(573, 873),
    source="Hydrogen-isotope transport in an ELBRODUR G CuCrZr alloy for nuclear applications in heat sinks, Journal of Nuclear Materials, Volume 473, May 2016, Pages 112–118",
    name="T Noh (2016)",
    author="noh",
    isotope="T",
    year=2016,
)

# ################# Anderl 1999 #############################
anderl_diffusivity_cucrzr_d = ArheniusProperty(
    2.0e-2,
    1.2,
    range=(700, 800),
    source="Deuterium transport in Cu, CuCrZr, and Cu/Be, Journal of Nuclear Materials 266-269 (1999) 761-765",
    name="D Anderl (1999)",
    author="anderl",
    isotope="D",
    year=1999,
)

# ################# Penalva 1999 #############################
penalva_diffusivity_cucrzr_h = ArheniusProperty(
    3.55e-5,
    65.5e3 * k_B / Rg,
    range=(593, 773),
    source="Interaction of Copper Alloys with Hydrogen, Copper Alloys – Early Applications and Current Performance – Enhancing Processes",
    name="D Penalva (1999)",
    isotope="D",
    author="penalva",
    year=1999,
)

penalva_solubility_cucrzr_h = ArheniusProperty(
    6.71e-3 * avogadro_nb,
    8.4e3 * k_B / Rg,
    range=(593, 773),
    source="Interaction of Copper Alloys with Hydrogen, Copper Alloys – Early Applications and Current Performance – Enhancing Processes",
    name="D Penalva (1999)",
    author="penalva",
    year=1999,
    isotope="D",
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
