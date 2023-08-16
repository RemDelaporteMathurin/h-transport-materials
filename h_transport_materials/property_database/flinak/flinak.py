import h_transport_materials as htm
from h_transport_materials.property import Diffusivity, Solubility, Permeability
import numpy as np

u = htm.ureg

# Fukada, 2006
data_fukada = np.genfromtxt(
    htm.absolute_path("fukada_2006/diffusivity/data_fukada_2006.csv"),
    delimiter=";",
)

fukada_diffusivity_h = Diffusivity(
    data_T=1 / data_fukada[:-1, 0] * u.K,
    data_y=data_fukada[:-1, 1] * u.m**2 * u.s**-1,
    source="fukada_hydrogen_2006",
    isotope="H",
    note="in original paper, the equation displayed on Fig 5 doesn't match the plotted line.",
)


data_fukada_S = np.genfromtxt(
    htm.absolute_path("fukada_2006/solubility/data_fukada_2006.csv"),
    delimiter=";",
)

fukada_solubility_h = Solubility(
    data_T=1 / data_fukada_S[:, 0] * u.K,
    data_y=data_fukada_S[:, 1] * u.mol * u.cm**-3 * u.atm**-1,
    source="fukada_hydrogen_2006",
    isotope="H",
)

# nakamura 2015
data_nakamura = np.genfromtxt(
    htm.absolute_path("nakamura_2015/data.csv"), delimiter=",", names=True
)

data_nakamura_diff_flinak_T = 1 / data_nakamura["diff_flinakx"] * u.K
data_nakamura_diff_flinak_y = data_nakamura["diff_flinaky"] * u.m**2 * u.s**-1

nakamura_diffusivity_h = Diffusivity(
    data_T=data_nakamura_diff_flinak_T,
    data_y=data_nakamura_diff_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
)

data_nakamura_sol_flinak_T = 1 / data_nakamura["sol_flinakx"] * u.K
data_nakamura_sol_flinak_y = (
    data_nakamura["sol_flinaky"] * u.mol * u.m**-3 * u.Pa**-1
)
nakamura_solubility_h = Solubility(
    data_T=data_nakamura_sol_flinak_T,
    data_y=data_nakamura_sol_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
)


data_nakamura_perm_flinak_T = 1 / data_nakamura["perm_flinakx"] * u.K
data_nakamura_perm_flinak_y = (
    data_nakamura["perm_flinaky"] * u.mol * u.m**-1 * u.s**-1 * u.Pa**-1
)
nakamura_permeability_h = Permeability(
    data_T=data_nakamura_perm_flinak_T,
    data_y=data_nakamura_perm_flinak_y,
    source="nakamura_hydrogen_2015",
    isotope="H",
)


# lam 2020
data_lam = np.genfromtxt(
    htm.absolute_path("lam_2020/data_lam_2020_t.csv"),
    delimiter=";",
)

lam_diffusivity_t = Diffusivity(
    data_T=1 / data_lam[:, 0] * u.K,
    data_y=data_lam[:, 1] * u.m**2 * u.s**-1,
    source="lam_impact_2021",
    isotope="T",
)

# T ions
data_lam_t_ions = np.genfromtxt(
    htm.absolute_path("lam_2020/data_lam_2020_t_ions.csv"), delimiter=";"
)

lam_diffusivity_t_ions = Diffusivity(
    data_T=1 / data_lam_t_ions[:, 0] * u.K,
    data_y=data_lam_t_ions[:, 1] * u.m**2 * u.s**-1,
    source="lam_impact_2021",
    isotope="T",
)

# Zeng 2019
data_zeng = np.genfromtxt(
    htm.absolute_path("zeng_2019/diffusivity/data_zeng_2019.csv"),
    delimiter=";",
)

zeng_diffusivity_h_2019 = Diffusivity(
    data_T=1 / data_zeng[:, 0] * u.K,
    data_y=data_zeng[:, 1] * u.m**2 * u.s**-1,
    source="zeng_behavior_2019",
    isotope="H",
    note="in original paper, the legend of Fig 5 is mixed up: red points correspond to Fukada and Morisaki.",
)

data_zeng_S = np.genfromtxt(
    htm.absolute_path("zeng_2019/solubility/data_zeng_2019.csv"),
    delimiter=";",
)
zeng_solubility_h_2019 = Solubility(
    data_T=1 / data_zeng_S[:, 0] * u.K,
    data_y=data_zeng_S[:, 1] * u.mol * u.m**-3 * u.Pa**-1,
    source="zeng_behavior_2019",
    isotope="H",
)


# zeng 2014

data_zeng_2014 = np.genfromtxt(
    htm.absolute_path("zeng_2014/diffusivity/data_zeng_2014.csv"),
    delimiter=";",
)

zeng_diffusivity_h_2014 = Diffusivity(
    data_T=data_zeng_2014[:, 0] * u.degC,
    data_y=data_zeng_2014[:, 1] * u.m**2 * u.s**-1,
    source="zeng_apparatus_2014",
    isotope="H",
)

data_zeng_2014_S = np.genfromtxt(
    htm.absolute_path("zeng_2014/solubility/data_zeng_2014.csv"),
    delimiter=";",
)


zeng_solubility_h_2014 = Solubility(
    data_T=data_zeng_2014_S[:, 0] * u.degC,
    data_y=data_zeng_2014_S[:, 1] * u.mol * u.m**-3 * u.Pa**-1,
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
