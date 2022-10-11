import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c
import numpy as np

SILVER_MOLAR_VOLUME = 1.03e-5  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/silver

katsuta_diffusivity = Diffusivity(
    D_0=8.55e-7,
    E_D=3.62e3 * htm.k_B,
    range=(947, 1123),
    source="katsuta_diffusivity_1979",
    isotope="H",
)


data_T_mclellan = np.array(
    [941.0, 921.0, 881.0, 857.0, 834.0, 810.0, 750.0, 727.0, 703.0]
)  # degC Table1
data_T_mclellan = data_T_mclellan + 273.15  # in Kelvin

data_y_mclellan = (
    np.array([6.17, 5.94, 4.24, 3.90, 3.15, 3.21, 2.25, 1.83, 1.51]) * 1e-6
)  # in at.fr Pa-1/2
data_y_mclellan *= htm.avogadro_nb / SILVER_MOLAR_VOLUME  # in m-3 Pa-1/2


mclellan_solubility = Solubility(
    data_T=data_T_mclellan,
    data_y=data_y_mclellan,
    units="m-3 Pa-1/2",
    source="mclellan_solid_1973",
    isotope="H",
    note="there is likely a mistake in Shimada's 2020 Review",
)

properties = [katsuta_diffusivity, mclellan_solubility]

for prop in properties:
    prop.material = "silver"

htm.database += properties
