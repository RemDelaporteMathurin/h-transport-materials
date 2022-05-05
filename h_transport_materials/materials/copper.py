from h_transport_materials import k_B, Rg
from h_transport_materials.property import ArheniusProperty
from h_transport_materials.materials import Material
from h_transport_materials.fitting import fit_arhenius

import numpy as np


reiter_src = "F. Reiter, K. S. Forcey, and G. Gervasini. A compilation of tritium : Material interaction parameters in fusion reactor materials. en. Publications Office of the European Union, July 1996."
reiter_diffusivity_copper = ArheniusProperty(pre_exp=6.6e-7, act_energy=0.39, source=reiter_src, name="T Reiter (1996)")
reiter_solubility = ArheniusProperty(pre_exp=3.14e24, act_energy=0.57, source=reiter_src, name="T Reiter (1996)")

magnusson_src = "Self-diffusion and impurity diffusion of hydrogen, oxygen, sulphur and phosphorus in copper, Magnusson & Firsk 2013"
magnusson_diffusivity_copper = ArheniusProperty(pre_exp=1.74e-6, act_energy=42000*k_B/Rg, source=magnusson_src, name="Magnusson (2013)")


# ################# KATZ 1971 #############################

katz_src = "Diffusion of H2, D2, and T2 in Single-Crystal Ni and Cu, PHYSICAL REVIEW B, VOLUM E 4, NUMBER 2, 15 JULY 1971"

data_diffusivity_katz = np.genfromtxt("h_transport_materials/materials/copper/katz_1971_diffusivity.csv", delimiter=",")
data_diffusivity_katz_h = data_diffusivity_katz[2:, :2].astype(float)

katz_diffusivity_copper_h = ArheniusProperty(
    *fit_arhenius(data_diffusivity_katz_h[:, 1]*1e-4, 1000/data_diffusivity_katz_h[:, 0]),
    source=katz_src, name="H Katz (1971)")


data_diffusivity_katz_d = data_diffusivity_katz[2:, 2:4][:-2].astype(float)
katz_diffusivity_copper_d = ArheniusProperty(
    *fit_arhenius(data_diffusivity_katz_d[:, 1]*1e-4, 1000/data_diffusivity_katz_d[:, 0]),
    source=katz_src, name="D Katz (1971)")


data_diffusivity_katz_t = data_diffusivity_katz[2:, 4:][:-2].astype(float)
katz_diffusivity_copper_t = ArheniusProperty(
    *fit_arhenius(data_diffusivity_katz_t[:, 1]*1e-4, 1000/data_diffusivity_katz_t[:, 0]),
    source=katz_src, name="T Katz (1971)")

copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility, name="copper")
