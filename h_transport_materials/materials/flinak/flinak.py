from h_transport_materials import k_B, avogadro_nb, Rg, diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from pathlib import Path
import numpy as np


# Fukada, 2006
data_fukada = np.genfromtxt(
    str(Path(__file__).parent) + "/fukada_2006/diffusivity/data_fukada_2006.csv",
    delimiter=";",
)

fukada_diffusivity_h = ArrheniusProperty(
    data_T=1 / data_fukada[:-1, 0],
    data_y=data_fukada[:-1, 1],
    source="fukada_hydrogen_2006",
    isotope="h",
)


data_fukada_S = np.genfromtxt(
    str(Path(__file__).parent) + "/fukada_2006/solubility/data_fukada_2006.csv",
    delimiter=";",
)

data_y_solubility_fukada = data_fukada_S[:, 1]  # mol/cm3/atm
data_y_solubility_fukada *= avogadro_nb  # /cm3/atm
data_y_solubility_fukada *= 1 / 101325  # /cm3/Pa
data_y_solubility_fukada *= 1e6  # /m3/Pa

fukada_solubility_h = Solubility(
    data_T=1 / data_fukada_S[:, 0],
    data_y=data_y_solubility_fukada,
    source="fukada_hydrogen_2006",
    isotope="h",
    units="m-3 Pa-1",
)

# nakamura 2015
data_nakamura_D = np.genfromtxt(
    str(Path(__file__).parent) + "/nakamura_2015/diffusivity/data_nakamura_2015.csv",
    delimiter=";",
)

nakamura_diffusivity_h = ArrheniusProperty(
    data_T=1 / data_nakamura_D[:, 0],
    data_y=data_nakamura_D[:, 1],
    source="nakamura_hydrogen_2015",
    isotope="h",
)

data_nakamura_S = np.genfromtxt(
    str(Path(__file__).parent) + "/nakamura_2015/solubility/data_nakamura_2015.csv",
    delimiter=";",
)
nakamura_solubility_h = Solubility(
    data_T=1 / data_nakamura_S[:, 0],
    data_y=data_nakamura_S[:, 1] * avogadro_nb,
    source="nakamura_hydrogen_2015",
    isotope="h",
    units="m-3 Pa-1",
)

# lam 2020
data_lam = np.genfromtxt(
    str(Path(__file__).parent) + "/lam_2020/data_lam_2020_t.csv", delimiter=";"
)

lam_diffusivity_t = ArrheniusProperty(
    data_T=1 / data_lam[:, 0],
    data_y=data_lam[:, 1],
    source="lam_impact_2021",
    isotope="t",
)

# T ions
data_lam_t_ions = np.genfromtxt(
    str(Path(__file__).parent) + "/lam_2020/data_lam_2020_t_ions.csv", delimiter=";"
)

lam_diffusivity_t_ions = ArrheniusProperty(
    data_T=1 / data_lam_t_ions[:, 0],
    data_y=data_lam_t_ions[:, 1],
    source="lam_impact_2021",
    isotope="t",
)

# Zeng 2019
data_zeng = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2019/diffusivity/data_zeng_2019.csv",
    delimiter=";",
)

zeng_diffusivity_h_2019 = ArrheniusProperty(
    data_T=1 / data_zeng[:, 0],
    data_y=data_zeng[:, 1],
    source="zeng_behavior_2019",
    isotope="h",
)

data_zeng_S = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2019/solubility/data_zeng_2019.csv",
    delimiter=";",
)
data_y_zeng_S = data_zeng_S[:, 1]  # in mol/m3/Pa
data_y_zeng_S *= avogadro_nb  # in /m3/Pa
zeng_solubility_h_2019 = Solubility(
    data_T=1 / data_zeng_S[:, 0],
    data_y=data_y_zeng_S,
    source="zeng_behavior_2019",
    isotope="h",
    units="m-3 Pa-1",
)


# zeng 2014

data_zeng_2014 = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2014/diffusivity/data_zeng_2014.csv",
    delimiter=";",
)

data_T_zeng_D = data_zeng_2014[:, 0]  # in °C
data_T_zeng_D += 273.15  # in K-1

zeng_diffusivity_h_2014 = ArrheniusProperty(
    data_T=data_T_zeng_D,
    data_y=data_zeng_2014[:, 1],
    source="zeng_apparatus_2014",
    isotope="h",
)

data_zeng_2014_S = np.genfromtxt(
    str(Path(__file__).parent) + "/zeng_2014/solubility/data_zeng_2014.csv",
    delimiter=";",
)

data_T_zeng_S = data_zeng_2014_S[:, 0]  # in °C
data_T_zeng_S += 273.15  # in K-1
data_y_zeng_S = data_zeng_2014_S[:, 1]  # in mol/m3/Pa
data_y_zeng_S *= avogadro_nb  # in /m3/Pa

zeng_solubility_h_2014 = Solubility(
    data_T=data_T_zeng_S,
    data_y=data_y_zeng_S,
    source="zeng_apparatus_2014",
    isotope="h",
    units="m-3 Pa-1",
)

flinak_diffusivities = [
    fukada_diffusivity_h,
    nakamura_diffusivity_h,
    lam_diffusivity_t,
    lam_diffusivity_t_ions,
    zeng_diffusivity_h_2014,
    zeng_diffusivity_h_2019,
]

flinak_solubilities = [
    nakamura_solubility_h,
    fukada_solubility_h,
    zeng_solubility_h_2019,
    zeng_solubility_h_2014,
]

for prop in flinak_diffusivities + flinak_solubilities:
    prop.material = "flinak"

diffusivities.properties += flinak_diffusivities
solubilities.properties += flinak_solubilities
