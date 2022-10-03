from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.conversion import kJ_per_mol_to_eV, atmn_to_Pan

from pathlib import Path
import numpy as np


LITHIUM_MOLAR_VOLUME = 1.3e-5  # m3/mol ref https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/lithium


alire_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/alire_1976/diffusivity.csv",
    delimiter=",",
)

alire_diffusivity_data_T = 1 / alire_diffusivity_data[:, 0]
alire_diffusivity_data_y = alire_diffusivity_data[:, 1] * 1e-4  # from cm2 to m2

# NOTE: in Shimada 2020, there is an error in Table 1 Lithium (lq.) line E_D column it should be 105.0 kJ/mol
alire_diffusivity = ArrheniusProperty(
    data_T=alire_diffusivity_data_T,
    data_y=alire_diffusivity_data_y,
    range=(898, 1178),
    isotope="H",
    source="alire_transport_1976",
)

veleckis_solubility = Solubility(
    pre_exp=atmn_to_Pan(np.exp(-6.498), n=-0.5) * avogadro_nb / LITHIUM_MOLAR_VOLUME,
    # pre_exp=1.75e-1 * avogadro_nb,
    act_energy=-6182 * k_B,
    range=(710 + 273.15, 903 + 273.15),
    source="veleckis_lithium-lithium_1974",
    isotope="H",
    units="m-3 Pa-1/2",
)

lithium_diffusivities = [alire_diffusivity]

lithium_solubilities = [veleckis_solubility]

for prop in lithium_diffusivities + lithium_solubilities:
    prop.material = "lithium"

diffusivities.properties += lithium_diffusivities
solubilities.properties += lithium_solubilities
