import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
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
)

# nakamura 2015
data_nakamura = np.genfromtxt(
    str(Path(__file__).parent) + "/nakamura_2015/data.csv", delimiter=",", names=True
)

data_nakamura_diff_flinak_T = 1 / data_nakamura["diff_flinakx"] * htm.ureg.K
data_nakamura_diff_flinak_y = (
    data_nakamura["diff_flinaky"] * htm.ureg.m**2 * htm.ureg.s**-1
)

nakamura_diffusivity_h = Diffusivity(
    data_T=data_nakamura_diff_flinak_T,
    data_y=data_nakamura_diff_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
)

data_nakamura_sol_flinak_T = 1 / data_nakamura["sol_flinakx"] * htm.ureg.K
data_nakamura_sol_flinak_y = (
    data_nakamura["sol_flinaky"] * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-1
)
nakamura_solubility_h = Solubility(
    data_T=data_nakamura_sol_flinak_T,
    data_y=data_nakamura_sol_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
)


data_nakamura_perm_flinak_T = 1 / data_nakamura["perm_flinakx"] * htm.ureg.K
data_nakamura_perm_flinak_y = (
    data_nakamura["perm_flinaky"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1
)
nakamura_permeability_h = Permeability(
    data_T=data_nakamura_perm_flinak_T,
    data_y=data_nakamura_perm_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
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
)

properties = [
    fukada_diffusivity_h,
    nakamura_diffusivity_h,
    nakamura_permeability_h,
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
    prop.material = htm.FLINAK

htm.database += properties
