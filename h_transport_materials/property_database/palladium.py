import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, RecombinationCoeff
import numpy as np

u = htm.ureg

PALLADIUM_VOLUMIC_DENSITY = (
    8.32e-8
    * u.m**3
    * u.g**-1  # m3/g  https://www.aqua-calc.com/calculate/weight-to-volume/palladium
)

volkl_diffusivity = Diffusivity(
    D_0=2.90e-7 * u.m**2 * u.s**-1,
    E_D=22.2 * u.kJ * u.mol**-1,
    range=(223 * u.K, 873 * u.K),
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
    * u.ccSTP
    * u.g**-1
    * u.cmHg**-0.5
)  # in cc STP per gram of palladium  cmHg^-1.2

favreau_data_y *= 1 / PALLADIUM_VOLUMIC_DENSITY  # mol T m-3  cmHg-1.2

favreau_solubility_t = Solubility(
    data_T=favreau_data_T * u.degC,
    data_y=favreau_data_y,
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
    * u.ccSTP
    * u.g**-1
    * u.cmHg**-0.5
)  # in cc STP per gram of palladium  cmHg^-1.2


favreau_data_y_h *= 1 / PALLADIUM_VOLUMIC_DENSITY  # mol T m-3  cmHg-1.2

favreau_solubility_h = Solubility(
    data_T=favreau_data_T_h * u.degC,
    data_y=favreau_data_y_h,
    source="favreau_solubility_1954",
    isotope="H",
)

data_inv_T_h = (
    np.array(
        [
            0.003354,
            0.003354,
            0.003354,
            0.003094,
            0.002679,
            0.002374,
            0.002113,
            0.001744,
            0.001485,
            0.001293,
            0.001293,
            0.001145,
            0.001027,
            0.000852,
        ]
    )
    * htm.ureg.K**-1
)

data_T_h = 1 / data_inv_T_h

# measured c_s
data_cs_h = (
    np.array(
        [
            1192.0,
            797.9,
            102.7,
            247.5,
            350.6,
            246.6,
            181.7,
            124.2,
            98.8,
            86.3,
            85.9,
            79.0,
            74.3,
            70.8,
        ]
    )
    * htm.ureg.mol
    * htm.ureg.m**-3
)

# Control pressure
data_P_h = (
    np.array(
        [
            1343.6,
            671.6,
            13.4,
            134.5,
            673.3,
            673.4,
            673.3,
            673.3,
            668.0,
            668.0,
            668.0,
            668.0,
            668.0,
            681.3,
        ]
    )
    * htm.ureg.Pa
)

data_solubility_h = data_cs_h / data_P_h**0.5

solubility_powell_h = htm.Solubility(
    data_T=data_T_h,
    data_y=data_solubility_h,
    isotope="H",
    note="table I, calculated from measured cs and control pressure columns",
    source="powell_surface_1991",
)


data_diffusivity_h = (
    np.array(
        [
            3.248e-11,
            3.339e-11,
            3.467e-11,
            7.056e-11,
            2.097e-10,
            4.870e-10,
            1.033e-9,
            2.910e-9,
            5.880e-9,
            9.943e-9,
            9.901e-9,
            1.482e-8,
            2.061e-8,
            3.286e-8,
        ]
    )
    * htm.ureg.m**2
    * htm.ureg.s**-1
)

diffusivity_powell_h = Diffusivity(
    data_T=data_T_h,
    data_y=data_diffusivity_h,
    isotope="H",
    note="table I, with h column",
    source="powell_surface_1991",
)

data_inv_T_D = (
    np.array(
        [
            0.003354,
            0.003354,
            0.003094,
            0.002679,
            0.002374,
            0.002113,
            0.001744,
            0.001485,
            0.001293,
            0.001145,
            0.001027,
            0.000852,
            0.000728,
        ]
    )
    * htm.ureg.K**-1
)

data_T_D = 1 / data_inv_T_D

# measured c_s
data_cs_D = (
    np.array(
        [
            352.2,
            108.4,
            273.1,
            184.2,
            141.6,
            114.8,
            103.5,
            71.4,
            66.6,
            63.4,
            62.1,
            62.3,
            63.1,
        ]
    )
    * htm.ureg.mol
    * htm.ureg.m**-3
)

# Control pressure
data_P_D = (
    np.array(
        [
            684.2,
            67.3,
            673.4,
            673.3,
            673.4,
            706.6,
            999.3,
            668.0,
            668.0,
            668.0,
            668.0,
            673.4,
            681.3,
        ]
    )
    * htm.ureg.Pa
)

data_solubility_D = data_cs_D / data_P_D**0.5

solubility_powell_d = htm.Solubility(
    data_T=data_T_D,
    data_y=data_solubility_D,
    isotope="D",
    note="table II, calculated from measured cs and control pressure columns",
    source="powell_surface_1991",
)

data_diffusivity_d = (
    np.array(
        [
            4.561e-11,
            4.601e-11,
            8.552e-11,
            2.395e-10,
            5.324e-10,
            1.037e-9,
            2.657e-9,
            4.933e-9,
            8.115e-9,
            1.218e-8,
            1.646e-8,
            2.572e-8,
            3.666e-8,
        ]
    )
    * htm.ureg.m**2
    * htm.ureg.s**-1
)

diffusivity_powell_d = Diffusivity(
    data_T=data_T_D,
    data_y=data_diffusivity_d,
    isotope="D",
    note="table II, with h column",
    source="powell_surface_1991",
)

takagi_recombination_d = RecombinationCoeff(
    pre_exp=1.5e-27 * u.m**4 * u.s**-1 * u.particle**-1,
    act_energy=0.48 * u.eV * u.particle**-1,
    range=(398 * u.K, 571 * u.K),
    isotope="D",
    source="takagi_asymmetric_2003",
    note="Equation 6",
)

properties = [
    volkl_diffusivity,
    favreau_solubility_t,
    favreau_solubility_h,
    solubility_powell_h,
    solubility_powell_d,
    diffusivity_powell_h,
    diffusivity_powell_d,
    takagi_recombination_d,
]

for prop in properties:
    prop.material = htm.PALLADIUM

htm.database += properties
