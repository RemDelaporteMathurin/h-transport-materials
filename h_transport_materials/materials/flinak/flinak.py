import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility
from pathlib import Path
import numpy as np


# Fukada, 2006
data_fukada = np.genfromtxt(
    str(Path(__file__).parent) + "/fukada_2006/diffusivity/data_fukada_2006.csv",
    delimiter=";",
)

fukada_diffusivity_h = Diffusivity(
    data_T=1 / data_fukada[:-1, 0] * htm.ureg.K,
    data_y=data_fukada[:-1, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="fukada_hydrogen_2006",
    isotope="H",
)


data_fukada_S = np.genfromtxt(
    str(Path(__file__).parent) + "/fukada_2006/solubility/data_fukada_2006.csv",
    delimiter=";",
)

fukada_solubility_h = Solubility(
    data_T=1 / data_fukada_S[:, 0] * htm.ureg.K,
    data_y=data_fukada_S[:, 1] * htm.ureg.mol * htm.ureg.cm**-3 * htm.ureg.atm**-1,
    source="fukada_hydrogen_2006",
    isotope="H",
    units="m-3 Pa-1",
)

# nakamura 2015
data_nakamura_D = np.genfromtxt(
    str(Path(__file__).parent) + "/nakamura_2015/diffusivity/data_nakamura_2015.csv",
    delimiter=";",
)

nakamura_diffusivity_h = Diffusivity(
    data_T=1 / data_nakamura_D[:, 0] * htm.ureg.K,
    data_y=data_nakamura_D[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="nakamura_hydrogen_2015",
    isotope="H",
)

data_nakamura_S = np.genfromtxt(
    str(Path(__file__).parent) + "/nakamura_2015/solubility/data_nakamura_2015.csv",
    delimiter=";",
)
nakamura_solubility_h = Solubility(
    data_T=1 / data_nakamura_S[:, 0] * htm.ureg.K,
    data_y=data_nakamura_S[:, 1] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    source="nakamura_hydrogen_2015",
    isotope="H",
    units="m-3 Pa-1",
)

# lam 2020
data_lam = np.genfromtxt(
    str(Path(__file__).parent) + "/lam_2020/data_lam_2020_t.csv", delimiter=";"
)

lam_diffusivity_t = Diffusivity(
    data_T=1 / data_lam[:, 0] * htm.ureg.K,
    data_y=data_lam[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="lam_impact_2021",
    isotope="T",
)

# T ions
data_lam_t_ions = np.genfromtxt(
    str(Path(__file__).parent) + "/lam_2020/data_lam_2020_t_ions.csv", delimiter=";"
)

lam_diffusivity_t_ions = Diffusivity(
    data_T=1 / data_lam_t_ions[:, 0] * htm.ureg.K,
    data_y=data_lam_t_ions[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="lam_impact_2021",
    isotope="T",
)

# Zeng 2019
data_zeng = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2019/diffusivity/data_zeng_2019.csv",
    delimiter=";",
)

zeng_diffusivity_h_2019 = Diffusivity(
    data_T=1 / data_zeng[:, 0] * htm.ureg.K,
    data_y=data_zeng[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="zeng_behavior_2019",
    isotope="H",
)

data_zeng_S = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2019/solubility/data_zeng_2019.csv",
    delimiter=";",
)
zeng_solubility_h_2019 = Solubility(
    data_T=1 / data_zeng_S[:, 0] * htm.ureg.K,
    data_y=data_zeng_S[:, 1] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    source="zeng_behavior_2019",
    isotope="H",
    units="m-3 Pa-1",
)


# zeng 2014

data_zeng_2014 = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2014/diffusivity/data_zeng_2014.csv",
    delimiter=";",
)

zeng_diffusivity_h_2014 = Diffusivity(
    data_T=data_zeng_2014[:, 0] * htm.ureg.degC,
    data_y=data_zeng_2014[:, 1] * htm.ureg.m**2 * htm.ureg.s**-1,
    source="zeng_apparatus_2014",
    isotope="H",
)

data_zeng_2014_S = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2014/solubility/data_zeng_2014.csv",
    delimiter=";",
)


zeng_solubility_h_2014 = Solubility(
    data_T=data_zeng_2014_S[:, 0] * htm.ureg.degC,
    data_y=data_zeng_2014_S[:, 1] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1,
    source="zeng_apparatus_2014",
    isotope="H",
    units="m-3 Pa-1",
)

properties = [
    fukada_diffusivity_h,
    nakamura_diffusivity_h,
    lam_diffusivity_t,
    lam_diffusivity_t_ions,
    zeng_diffusivity_h_2014,
    zeng_diffusivity_h_2019,
    nakamura_solubility_h,
    fukada_solubility_h,
    zeng_solubility_h_2019,
    zeng_solubility_h_2014,
]

for prop in properties:
    prop.material = "flinak"

htm.database += properties
