from h_transport_materials import k_B, Rg, diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials.materials import Material
from pathlib import Path
import numpy as np


cited_in_database_for_ITER = "cited in Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials"

# ################# REITER 1996 #############################

reiter_diffusivity_copper = ArrheniusProperty(
    pre_exp=6.6e-7,
    act_energy=0.39,
    range=(470, 1200),
    source="reiter_compilation_1996",
    name="T Reiter (1996)",
    isotope="T",
)
reiter_solubility_copper = Solubility(
    pre_exp=3.14e24,
    act_energy=0.57,
    range=(470, 1200),
    source="reiter_compilation_1996",
    name="T Reiter (1996)",
    isotope="T",
    units="m-3 Pa-1/2",
)

# copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility_copper, name="copper")


magnusson_diffusivity_copper = ArrheniusProperty(
    pre_exp=1.74e-6,
    act_energy=42000 * k_B / Rg,
    range=(298, 1273),
    source="magnusson_self-diffusion_2013",
    name="H Magnusson (2013)",
    isotope="H",
)


# ################# KATZ 1971 #############################

katz_src = "katz_diffusion_1971"
data_diffusivity_katz = np.genfromtxt(
    str(Path(__file__).parent) + "/katz_1971_diffusivity.csv",
    delimiter=",",
)
data_diffusivity_katz_h = data_diffusivity_katz[2:, :2].astype(float)

katz_diffusivity_copper_h = ArrheniusProperty(
    data_T=1000 / data_diffusivity_katz_h[:, 0],
    data_y=data_diffusivity_katz_h[:, 1] * 1e-4,
    source=katz_src,
    name="H Katz (1971)",
    isotope="H",
)


data_diffusivity_katz_d = data_diffusivity_katz[2:, 2:4][:-2].astype(float)
katz_diffusivity_copper_d = ArrheniusProperty(
    data_T=1000 / data_diffusivity_katz_d[:, 0],
    data_y=data_diffusivity_katz_d[:, 1] * 1e-4,
    source=katz_src,
    name="D Katz (1971)",
    isotope="D",
)


data_diffusivity_katz_t = data_diffusivity_katz[2:, 4:][:-2].astype(float)
katz_diffusivity_copper_t = ArrheniusProperty(
    data_T=1000 / data_diffusivity_katz_t[:, 0],
    data_y=data_diffusivity_katz_t[:, 1] * 1e-4,
    source=katz_src,
    name="T Katz (1971)",
    isotope="T",
)

# ################# Eichenauer 1957 #############################
eichenauer_diffusivity_copper_h = ArrheniusProperty(
    1.1e-6,
    0.4,
    range=(700, 920),
    source="eichenauer_notitle_1957",
    name="H Eichenauer (1957)",
    isotope="H",
)

eichenauer_solubility_copper_h = Solubility(
    pre_exp=4.9e23,
    act_energy=0.37,
    range=(700, 920),
    source="eichenauer_notitle_1957",
    name="H Eichenauer (1957)",
    isotope="H",
    units="m-3 Pa-1/2",
)

# ################# Perkins 1973 #############################
perkins_diffusivity_copper_h = ArrheniusProperty(
    1.06e-6,
    0.4,
    range=(410, 710),
    source="perkins_permeation_1973",
    name="H Perkins (1973)",
    isotope="H",
)

# ################# Tanabe 1987 #############################
# from Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials
tanabe_diffusivity_copper_d = ArrheniusProperty(
    6.7e-8,
    0.24,
    range=(298, 1070),
    source="tanabe_hydrogen_1987",
    name="D Tanabe (1987)",
    isotope="D",
)

# ################# Eichenauer 1965 #############################
eichenauer_diffusivity_copper_d = ArrheniusProperty(
    6.19e-7,
    0.392,
    range=(703, 913),
    source="eichenauer_notitle_1965",
    name="D Eichenauer (1965)",
    isotope="D",
)

eichenauer_solubility_copper_d = Solubility(
    pre_exp=3.19e24,
    act_energy=0.41,
    range=(703, 913),
    source="eichenauer_notitle_1965",
    name="D Eichenauer (1965)",
    isotope="D",
    units="m-3 Pa-1/2",
)

# ################# Anderl 1990 #############################
anderl_diffusivity_copper_d = ArrheniusProperty(
    9.26e-7,
    0.409,
    range=(638, 723),
    source="anderl_hydrogen_1990",
    name="D Anderl (1990)",
    isotope="D",
)


# ################# Anderl 1999 #############################
anderl_diffusivity_copper_d_1999 = ArrheniusProperty(
    2.1e-6,
    0.52,
    range=(700, 800),
    source="anderl_deuterium_1999",
    name="D Anderl (1999)",
    isotope="D",
)


# ################# Sakamoto 1982 #############################
sakamoto_diffusivity_copper_h = ArrheniusProperty(
    3.69e-7,
    36820 * k_B / Rg,
    range=(292, 339),
    source="sakamoto_electrochemical_1982",
    name="H Sakamoto (1982)",
    isotope="H",
)

# ################# Otsuka 2010 #############################
otsuka_diffusivity_copper_t = ArrheniusProperty(
    1.11e-6,
    0.399,
    range=(303, 353),
    source="otsuka_behavior_2010",
    name="T Otsuka (1982)",
    isotope="T",
)

# ################# Thomas 1967 #############################
thomas_solubility_copper_h = Solubility(
    pre_exp=1.90e24,
    act_energy=0.51,
    range=(770, 1320),
    source="thomas_solubility_1967",
    name="H Thomas (1967)",
    isotope="H",
    units="m-3 Pa-1/2",
)

# ################# Wampler 1976 #############################
wampler_solubility_copper_h = Solubility(
    pre_exp=1.07e24,
    act_energy=0.44,
    range=(770, 1070),
    source="wampler_precipitation_1976",
    name="H Wampler (1976)",
    isotope="H",
    units="m-3 Pa-1/2",
)


copper_diffusivities = [
    reiter_diffusivity_copper,
    magnusson_diffusivity_copper,
    katz_diffusivity_copper_h,
    katz_diffusivity_copper_d,
    katz_diffusivity_copper_t,
    eichenauer_diffusivity_copper_h,
    perkins_diffusivity_copper_h,
    tanabe_diffusivity_copper_d,
    eichenauer_diffusivity_copper_d,
    anderl_diffusivity_copper_d,
    anderl_diffusivity_copper_d_1999,
    sakamoto_diffusivity_copper_h,
    otsuka_diffusivity_copper_t,
]

copper_solubilities = [
    reiter_solubility_copper,
    eichenauer_solubility_copper_d,
    thomas_solubility_copper_h,
    wampler_solubility_copper_h,
    eichenauer_solubility_copper_h,
]

for prop in copper_diffusivities + copper_solubilities:
    prop.material = "copper"

diffusivities.properties += copper_diffusivities
solubilities.properties += copper_solubilities
