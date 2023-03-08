from h_transport_materials.property import Diffusivity, Solubility
import h_transport_materials as htm
from h_transport_materials import k_B, Rg, avogadro_nb

from pathlib import Path
import numpy as np


LITHIUM_MOLAR_VOLUME = (
    1.3e-5 * htm.ureg.m**3 * htm.ureg.mol**-1
)  # m3/mol ref https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/lithium


alire_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/alire_1976/diffusivity.csv",
    delimiter=",",
)


alire_diffusivity = Diffusivity(
    data_T=(1 / alire_diffusivity_data[:, 0]) * htm.ureg.K,
    data_y=alire_diffusivity_data[:, 1] * htm.ureg.cm**2 * htm.ureg.s**-1,
    range=(898 * htm.ureg.K, 1178 * htm.ureg.K),
    isotope="H",
    source="alire_transport_1976",
    note="in Shimada 2020, there is an error in Table 1 Lithium (lq.) line E_D column it should be 105.0 kJ/mol",
)

veleckis_solubility = Solubility(
    S_0=np.exp(-6.498) / LITHIUM_MOLAR_VOLUME * htm.ureg.atm**-0.5,
    # S_0=1.75e-1 * avogadro_nb,
    E_S=-6182 * htm.ureg.K * k_B,
    range=(
        htm.ureg.Quantity(710, htm.ureg.degC),
        htm.ureg.Quantity(903, htm.ureg.degC),
    ),
    source="veleckis_lithium-lithium_1974",
    isotope="H",
    note="table 1 of original paper",
)


smith_sol_data_y_h = htm.ureg.Quantity(
    [31.0, 42.0, 56.0, 74.0, 93.0, 110.0, 137.0],
    htm.ureg.torr**0.5 * htm.ureg.mol / htm.ureg.mol,
)
smith_sol_data_y_h **= -1
smith_sol_data_y_h *= 1 / LITHIUM_MOLAR_VOLUME

smith_solubility_h = Solubility(
    data_T=htm.ureg.Quantity([700, 750, 800, 850, 900, 950, 1000], htm.ureg.degC),
    data_y=smith_sol_data_y_h,
    isotope="H",
    source="smith_solubility_1979",
    note="table 1 of original paper",
)


smith_sol_data_y_d = htm.ureg.Quantity(
    [41.0, 54.0, 76.0, 88.0, 112.0, 134.0, 160.0],
    htm.ureg.torr**0.5 * htm.ureg.mol / htm.ureg.mol,
)
smith_sol_data_y_d **= -1
smith_sol_data_y_d *= 1 / LITHIUM_MOLAR_VOLUME

smith_solubility_d = Solubility(
    data_T=htm.ureg.Quantity([700, 750, 800, 850, 900, 950, 1000], htm.ureg.degC),
    data_y=smith_sol_data_y_d,
    isotope="D",
    source="smith_solubility_1979",
    note="table 1 of original paper",
)


smith_sol_data_y_t = htm.ureg.Quantity(
    [57.0, 71.0, 89.0, 108.0, 130.0, 160.0, 190.0],
    htm.ureg.torr**0.5 * htm.ureg.mol / htm.ureg.mol,
)
smith_sol_data_y_t **= -1
smith_sol_data_y_t *= 1 / LITHIUM_MOLAR_VOLUME

smith_solubility_t = Solubility(
    data_T=htm.ureg.Quantity([700, 750, 800, 850, 900, 950, 1000], htm.ureg.degC),
    data_y=smith_sol_data_y_t,
    isotope="T",
    source="smith_solubility_1979",
    note="table 1 of original paper",
)


properties = [
    alire_diffusivity,
    veleckis_solubility,
    smith_solubility_h,
    smith_solubility_d,
    smith_solubility_t,
]

for prop in properties:
    prop.material = htm.LITHIUM

htm.database += properties
