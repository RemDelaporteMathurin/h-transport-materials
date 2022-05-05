from h_transport_materials import k_B, Rg
from h_transport_materials.property import ArheniusProperty
from h_transport_materials.materials import Material

import numpy as np


cited_in_database_for_ITER = "cited in Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials"

# ################# REITER 1996 #############################

reiter_src = "F. Reiter, K. S. Forcey, and G. Gervasini. A compilation of tritium : Material interaction parameters in fusion reactor materials. en. Publications Office of the European Union, July 1996."
reiter_diffusivity_copper = ArheniusProperty(
    pre_exp=6.6e-7, act_energy=0.39,
    range=(470, 1200),
    source=reiter_src, name="T Reiter (1996)")
reiter_solubility = ArheniusProperty(
    pre_exp=3.14e24, act_energy=0.57,
    range=(470, 1200),
    source=reiter_src, name="T Reiter (1996)")

copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility, name="copper")


magnusson_src = "Self-diffusion and impurity diffusion of hydrogen, oxygen, sulphur and phosphorus in copper, Magnusson & Firsk 2013"
magnusson_diffusivity_copper = ArheniusProperty(
    pre_exp=1.74e-6, act_energy=42000*k_B/Rg,
    range=(298, 1273),
    source=magnusson_src, name="H Magnusson (2013)")


# ################# KATZ 1971 #############################

katz_src = "Diffusion of H2, D2, and T2 in Single-Crystal Ni and Cu, PHYSICAL REVIEW B, VOLUM E 4, NUMBER 2, 15 JULY 1971"

data_diffusivity_katz = np.genfromtxt("h_transport_materials/materials/copper/katz_1971_diffusivity.csv", delimiter=",")
data_diffusivity_katz_h = data_diffusivity_katz[2:, :2].astype(float)

katz_diffusivity_copper_h = ArheniusProperty(
    data_T=1000/data_diffusivity_katz_h[:, 0],
    data_y=data_diffusivity_katz_h[:, 1]*1e-4,
    source=katz_src, name="H Katz (1971)")


data_diffusivity_katz_d = data_diffusivity_katz[2:, 2:4][:-2].astype(float)
katz_diffusivity_copper_d = ArheniusProperty(
    data_T=1000/data_diffusivity_katz_d[:, 0],
    data_y=data_diffusivity_katz_d[:, 1]*1e-4,
    source=katz_src, name="D Katz (1971)")


data_diffusivity_katz_t = data_diffusivity_katz[2:, 4:][:-2].astype(float)
katz_diffusivity_copper_t = ArheniusProperty(
    data_T=1000/data_diffusivity_katz_t[:, 0],
    data_y=data_diffusivity_katz_t[:, 1]*1e-4,
    source=katz_src, name="T Katz (1971)")

# ################# Eichenauer 1957 #############################
eichenauer_diffusivity_copper_h = ArheniusProperty(
    1.1e-6, 0.4, range=(700, 920),
    source=cited_in_database_for_ITER, name="H Eichenauer (1957)")

# ################# Perkins 1973 #############################
perkins_diffusivity_copper_h = ArheniusProperty(
    1.06e-6, 0.4, range=(410, 710),
    source=cited_in_database_for_ITER, name="H Perkins (1957)")

# ################# Perkins 1973 #############################
tanabe_diffusivity_copper_d = ArheniusProperty(
    6.7e-8, 0.24, range=(298, 1070),
    source=cited_in_database_for_ITER, name="D Tanabe (1987)")

# ################# Eichenauer 1965 #############################
eichenauer_diffusivity_copper_d = ArheniusProperty(
    6.19e-7, 0.392, range=(703, 913),
    source="Z. Metallkd., 56 (1965), p. 287",
    name="D Eichenauer (1965)")

# ################# Anderl 1990 #############################
anderl_diffusivity_copper_d = ArheniusProperty(
    9.26e-7, 0.409, range=(638, 723),
    source="Hydrogen transport behavior of metal coatings for plasma-facing components, Journal of Nuclear Materials, Volumes 176–177, 3 December 1990, Pages 683-689",
    name="D Anderl (1990)")


# ################# Anderl 1999 #############################
anderl_diffusivity_copper_d_1999 = ArheniusProperty(
    2.1e-6, 0.52, range=(700, 800),
    source="Deuterium transport in Cu, CuCrZr, and Cu/Be, Journal of Nuclear Materials 266-269 (1999) 761-765",
    name="D Anderl (1999)")


# ################# Sakamoto 1982 #############################
sakamoto_diffusivity_copper_h = ArheniusProperty(
    3.69e-7, 36820*k_B/Rg, range=(292, 339),
    source="The Electrochemical Determination of  Diffusivity and Solubility of Hydrogen in Copper, J.Japan Inst.Metals, Vol.46, No.3(1982), pp. 285-290",
    name="H Sakamoto (1982)")

# ################# Otsuka 2010 #############################
otsuka_diffusivity_copper_t = ArheniusProperty(
    1.11e-6, 0.399, range=(303, 353),
    source="Behavior of tritium accumulated on materials surface, Fusion Engineering and Design, Volume 85, Issues 7–9, December 2010, Pages 1437–1441",
    name="T Otsuka (1982)")
