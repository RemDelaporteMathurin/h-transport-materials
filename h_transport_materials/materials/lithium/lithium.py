from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.conversion import kJ_per_mol_to_eV

from pathlib import Path
import numpy as np

alire_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/alire_1976/diffusivity.csv",
    delimiter=",",
)

alire_diffusivity_data_T = 1 / alire_diffusivity_data[:, 0]
alire_diffusivity_data_y = alire_diffusivity_data[:, 1] * 1e-4  # from cm2 to m2

alire_diffusivity = ArrheniusProperty(
    data_T=alire_diffusivity_data_T,
    data_y=alire_diffusivity_data_y,
    range=(898, 1178),
    # source=frauenfelder_src,
    name="Alire (1976)",
    isotope="H",
    author="alire",
    year=1976,
)
# NOTE: in Shimada 2020, there is an error in Table 1 Lithium (lq.) line E_D column it should be 105.0 kJ/mol


veleckis_solubility = ArrheniusProperty(pre_exp=1)

lithium_diffusivities = [alire_diffusivity]

lithium_solubilities = []

for prop in lithium_diffusivities + lithium_solubilities:
    prop.material = "lithium"

diffusivities.properties += lithium_diffusivities
solubilities.properties += lithium_solubilities
