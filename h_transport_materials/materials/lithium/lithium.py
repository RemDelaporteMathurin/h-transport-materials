from h_transport_materials.property import Diffusivity, Solubility
import h_transport_materials as htm
from h_transport_materials import k_B, Rg, avogadro_nb

from pathlib import Path
import numpy as np


LITHIUM_MOLAR_VOLUME = 1.3e-5  # m3/mol ref https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/lithium


alire_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/alire_1976/diffusivity.csv",
    delimiter=",",
)


alire_diffusivity = Diffusivity(
    data_T=(1 / alire_diffusivity_data[:, 0]) * htm.ureg.K,
    data_y=alire_diffusivity_data[:, 1] * htm.ureg.cm**2 * htm.ureg.s**-1,
    range=(898, 1178),
    isotope="H",
    source="alire_transport_1976",
    note="in Shimada 2020, there is an error in Table 1 Lithium (lq.) line E_D column it should be 105.0 kJ/mol",
)

veleckis_solubility = Solubility(
    S_0=np.exp(-6.498)
    / LITHIUM_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.atm**-0.5,
    # S_0=1.75e-1 * avogadro_nb,
    E_S=-6182 * k_B * htm.ureg.eV * htm.ureg.particle**-1,
    range=(710 + 273.15, 903 + 273.15),
    source="veleckis_lithium-lithium_1974",
    isotope="H",
    units="m-3 Pa-1/2",
)

properties = [alire_diffusivity, veleckis_solubility]

for prop in properties:
    prop.material = "lithium"

htm.database += properties
