import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

import numpy as np

PALLADIUM_MOLAR_VOLUME = (
    8.85e-6 * htm.ureg.m**3 * htm.ureg.mol**-1
)  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/palladium
PALLADIUM_VOLUMIC_DENSITY = (
    8.32e-8
    * htm.ureg.m**3
    * htm.ureg.g
    ** -1  # m3/g  https://www.aqua-calc.com/calculate/weight-to-volume/palladium
)

volkl_diffusivity = Diffusivity(
    D_0=2.90e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=22.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(223 * htm.ureg.K, 873 * htm.ureg.K),
    source="volkl_5_1975",
    isotope="H",
)


favreau_data_T = np.array(
    [
        200.75,
        306.0,
        400.0,
        200.5,
        305.0,
        399.5,
        398.25,
        400.0,
        402.0,
        395.65,
        399.5,
        401.5,
        298.5,
        296.38,
        305.5,
        298.0,
        300.0,
        199.5,
        201.2,
        205.33,
        200.25,
        303.0,
        401.25,
    ]
)  # in degC Table II


favreau_data_y = (
    np.array(
        [
            0.17225,
            0.17470,
            0.1066,
            0.12335,
            0.1267,
            0.1227,
            0.1343,
            0.12515,
            0.1089,
            0.1083,
            0.1173,
            0.1004,
            0.1045,
            0.11095,
            0.1038,
            0.1073,
            0.1298,
            0.1205,
            0.1255,
            0.1292,
            0.1285,
            0.1219,
            0.1039,
        ]
    )
    * htm.ureg.ccSTP
    * htm.ureg.g**-1
    * htm.ureg.cmHg**-0.5
)  # in cc STP per gram of palladium  cmHg^-1.2

# favreau_data_y = c.ccSTP_to_mol(favreau_data_y)  # mol T per gram of Pd  cmHg-1.2
favreau_data_y *= 1 / PALLADIUM_VOLUMIC_DENSITY  # mol T m-3  cmHg-1.2

favreau_solubility_t = Solubility(
    data_T=favreau_data_T * htm.ureg.degC,
    data_y=favreau_data_y,
    # S_0=4.45e-1 * htm.avogadro_nb,
    # E_S=c.kJ_per_mol_to_eV(-8.4),
    source="favreau_solubility_1954",
    isotope="T",
)

favreau_data_T_h = np.array(
    [
        196.5,
        301.2,
        202.5,
        304.5,
        409.7,
        202.0,
        303.75,
        405.0,
        205.0,
        306.2,
        403.3,
        203.0,
        304.5,
        403.0,
        200.6,
        302.75,
        406.5,
        203.25,
        304.5,
        402.0,
        206.0,
        308.0,
        405.0,
        200.0,
        309.5,
        306.0,
        403.0,
        199.0,
        305.5,
        199.0,
        306.0,
        403.0,
        199.0,
        304.0,
        399.0,
        198.0,
        306.0,
        403.0,
        199.0,
        304.0,
        402.0,
        194.5,
        301.0,
        398.0,
        304.0,
        200.0,
        302.0,
        403.0,
        200.5,
        306.0,
        402.0,
        200.0,
        306.0,
        402.0,
        198.0,
        306.0,
        404.0,
        196.0,
        303.0,
        402.0,
        196.5,
        303.0,
        405.5,
        200.0,
        403.5,
        305.5,
    ]
)  # in degC


favreau_data_y_h = (
    np.array(
        [
            0.2519,
            0.2060,
            0.2528,
            0.1665,
            0.1246,
            0.2521,
            0.1690,
            0.1484,
            0.2184,
            0.1457,
            0.1103,
            0.2218,
            0.1804,
            0.1426,
            0.2593,
            0.1667,
            0.1245,
            0.2577,
            0.1860,
            0.1396,
            0.2408,
            0.1556,
            0.1103,
            0.3084,
            0.2144,
            0.2039,
            0.1456,
            0.2452,
            0.2006,
            0.2634,
            0.1666,
            0.1465,
            0.2483,
            0.1696,
            0.1324,
            0.2383,
            0.1657,
            0.1248,
            0.2563,
            0.1787,
            0.1361,
            0.2617,
            0.1701,
            0.1427,
            0.1824,
            0.2609,
            0.1847,
            0.1422,
            0.2729,
            0.1690,
            0.1273,
            0.2581,
            0.1711,
            0.1365,
            0.2579,
            0.1663,
            0.1223,
            0.2589,
            0.1793,
            0.1430,
            0.2587,
            0.1706,
            0.1369,
            0.2603,
            0.1300,
            0.1767,
        ]
    )
    * htm.ureg.ccSTP
    * htm.ureg.g**-1
    * htm.ureg.cmHg**-0.5
)  # in cc STP per gram of palladium  cmHg^-1.2


favreau_data_y_h *= 1 / PALLADIUM_VOLUMIC_DENSITY  # mol T m-3  cmHg-1.2

favreau_solubility_h = Solubility(
    data_T=favreau_data_T_h * htm.ureg.degC,
    data_y=favreau_data_y_h,
    source="favreau_solubility_1954",
    isotope="H",
)

properties = [volkl_diffusivity, favreau_solubility_t, favreau_solubility_h]

for prop in properties:
    prop.material = htm.PALLADIUM

htm.database += properties
