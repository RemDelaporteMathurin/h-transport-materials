from h_transport_materials import k_B, Rg, diffusivities, solubilities
from h_transport_materials.property import ArheniusProperty
from h_transport_materials.materials import Material
import numpy as np


cited_in_database_for_ITER = "cited in Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials"

# ################# REITER 1996 #############################

reiter_src = "F. Reiter, K. S. Forcey, and G. Gervasini. A compilation of tritium : Material interaction parameters in fusion reactor materials. en. Publications Office of the European Union, July 1996."
reiter_diffusivity_copper = ArheniusProperty(
    pre_exp=6.6e-7,
    act_energy=0.39,
    range=(470, 1200),
    source=reiter_src,
    name="T Reiter (1996)",
    year=1996,
    isotope="T",
    author="reiter",
)
reiter_solubility_copper = ArheniusProperty(
    pre_exp=3.14e24,
    act_energy=0.57,
    range=(470, 1200),
    source=reiter_src,
    name="T Reiter (1996)",
    year=1996,
    isotope="T",
    author="reiter",
)

# copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility_copper, name="copper")


magnusson_src = "Self-diffusion and impurity diffusion of hydrogen, oxygen, sulphur and phosphorus in copper, Magnusson & Firsk 2013"
magnusson_diffusivity_copper = ArheniusProperty(
    pre_exp=1.74e-6,
    act_energy=42000 * k_B / Rg,
    range=(298, 1273),
    source=magnusson_src,
    name="H Magnusson (2013)",
    isotope="H",
    year=2013,
    author="magnusson",
)


# ################# KATZ 1971 #############################

katz_src = "Diffusion of H2, D2, and T2 in Single-Crystal Ni and Cu, PHYSICAL REVIEW B, VOLUM E 4, NUMBER 2, 15 JULY 1971"

data_diffusivity_katz = np.genfromtxt(
    "h_transport_materials/materials/copper/katz_1971_diffusivity.csv", delimiter=","
)
data_diffusivity_katz_h = data_diffusivity_katz[2:, :2].astype(float)

katz_diffusivity_copper_h = ArheniusProperty(
    data_T=1000 / data_diffusivity_katz_h[:, 0],
    data_y=data_diffusivity_katz_h[:, 1] * 1e-4,
    source=katz_src,
    name="H Katz (1971)",
    year=1971,
    isotope="H",
    author="katz",
)


data_diffusivity_katz_d = data_diffusivity_katz[2:, 2:4][:-2].astype(float)
katz_diffusivity_copper_d = ArheniusProperty(
    data_T=1000 / data_diffusivity_katz_d[:, 0],
    data_y=data_diffusivity_katz_d[:, 1] * 1e-4,
    source=katz_src,
    name="D Katz (1971)",
    year=1971,
    isotope="D",
    author="katz",
)


data_diffusivity_katz_t = data_diffusivity_katz[2:, 4:][:-2].astype(float)
katz_diffusivity_copper_t = ArheniusProperty(
    data_T=1000 / data_diffusivity_katz_t[:, 0],
    data_y=data_diffusivity_katz_t[:, 1] * 1e-4,
    source=katz_src,
    name="T Katz (1971)",
    year=1971,
    isotope="T",
    author="katz",
)

# ################# Eichenauer 1957 #############################
eichenauer_diffusivity_copper_h = ArheniusProperty(
    1.1e-6,
    0.4,
    range=(700, 920),
    source=cited_in_database_for_ITER,
    name="H Eichenauer (1957)",
    year=1957,
    isotope="H",
    author="eichenauer",
)

eichenauer_solubility_copper_h = ArheniusProperty(
    4.9e23,
    0.37,
    range=(700, 920),
    source=cited_in_database_for_ITER,
    name="H Eichenauer (1957)",
    year=1957,
    isotope="H",
    author="eichenauer",
)

# ################# Perkins 1973 #############################
perkins_diffusivity_copper_h = ArheniusProperty(
    1.06e-6,
    0.4,
    range=(410, 710),
    source=cited_in_database_for_ITER,
    name="H Perkins (1957)",
    year=1957,
    isotope="H",
    author="perkins",
)

# ################# Perkins 1973 #############################
tanabe_diffusivity_copper_d = ArheniusProperty(
    6.7e-8,
    0.24,
    range=(298, 1070),
    source=cited_in_database_for_ITER,
    name="D Tanabe (1987)",
    year=1987,
    isotope="D",
    author="tanabe",
)

# ################# Eichenauer 1965 #############################
eichenauer_diffusivity_copper_d = ArheniusProperty(
    6.19e-7,
    0.392,
    range=(703, 913),
    source="Z. Metallkd., 56 (1965), p. 287",
    name="D Eichenauer (1965)",
    year=1965,
    isotope="D",
    author="eichenauer",
)

eichenauer_solubility_copper_d = ArheniusProperty(
    3.19e24,
    0.41,
    range=(703, 913),
    source="Z. Metallkd., 56 (1965), p. 287",
    name="D Eichenauer (1965)",
    year=1965,
    isotope="D",
    author="eichenauer",
)

# ################# Anderl 1990 #############################
anderl_diffusivity_copper_d = ArheniusProperty(
    9.26e-7,
    0.409,
    range=(638, 723),
    source="Hydrogen transport behavior of metal coatings for plasma-facing components, Journal of Nuclear Materials, Volumes 176–177, 3 December 1990, Pages 683-689",
    name="D Anderl (1990)",
    year=1990,
    isotope="D",
    author="anderl",
)


# ################# Anderl 1999 #############################
anderl_diffusivity_copper_d_1999 = ArheniusProperty(
    2.1e-6,
    0.52,
    range=(700, 800),
    source="Deuterium transport in Cu, CuCrZr, and Cu/Be, Journal of Nuclear Materials 266-269 (1999) 761-765",
    name="D Anderl (1999)",
    year=1999,
    isotope="D",
    author="anderl",
)


# ################# Sakamoto 1982 #############################
sakamoto_diffusivity_copper_h = ArheniusProperty(
    3.69e-7,
    36820 * k_B / Rg,
    range=(292, 339),
    source="The Electrochemical Determination of  Diffusivity and Solubility of Hydrogen in Copper, J.Japan Inst.Metals, Vol.46, No.3(1982), pp. 285-290",
    name="H Sakamoto (1982)",
    year=1982,
    isotope="H",
    author="sakamoto",
)

# ################# Otsuka 2010 #############################
otsuka_diffusivity_copper_t = ArheniusProperty(
    1.11e-6,
    0.399,
    range=(303, 353),
    source="Behavior of tritium accumulated on materials surface, Fusion Engineering and Design, Volume 85, Issues 7–9, December 2010, Pages 1437–1441",
    name="T Otsuka (1982)",
    year=1982,
    isotope="T",
    author="otsuka",
)

# ################# Thomas 1967 #############################
thomas_solubility_copper_h = ArheniusProperty(
    1.90e24,
    0.51,
    range=(770, 1320),
    source=cited_in_database_for_ITER,
    name="H Thomas (1967)",
    year=1967,
    isotope="H",
    author="thomas",
)

# ################# Wampler 1976 #############################
wampler_solubility_copper_h = ArheniusProperty(
    1.07e24,
    0.44,
    range=(770, 1070),
    source=cited_in_database_for_ITER,
    name="H Wampler (1976)",
    year=1976,
    isotope="H",
    author="wampler",
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
