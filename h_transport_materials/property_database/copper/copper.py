from h_transport_materials import k_B, Rg, avogadro_nb
import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    Permeability,
    RecombinationCoeff,
    Solubility,
)
from pathlib import Path
import numpy as np

COPPER_MOLAR_VOLUME = 7.11e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/copper

# ################# REITER 1996 #############################

reiter_diffusivity_copper = Diffusivity(
    D_0=6.6e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.39 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(470 * htm.ureg.K, 1200 * htm.ureg.K),
    source="reiter_compilation_1996",
    isotope="T",
)
reiter_solubility_copper = Solubility(
    S_0=3.14e24 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.57 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(470 * htm.ureg.K, 1200 * htm.ureg.K),
    source="reiter_compilation_1996",
    isotope="T",
)

# copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility_copper, name="copper")


magnusson_diffusivity_copper = Diffusivity(
    D_0=1.74e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=42000 * htm.ureg.J * htm.ureg.mol**-1,
    range=(298 * htm.ureg.K, 1273 * htm.ureg.K),
    source="magnusson_self-diffusion_2013",
    isotope="H",
)


# ################# KATZ 1971 #############################

katz_src = "katz_diffusion_1971"
data_diffusivity_katz = np.genfromtxt(
    str(Path(__file__).parent) + "/katz_1971_diffusivity.csv",
    delimiter=",",
)
data_diffusivity_katz_h = data_diffusivity_katz[2:, :2].astype(float)

katz_diffusivity_copper_h = Diffusivity(
    data_T=1000 / data_diffusivity_katz_h[:, 0] * htm.ureg.K,
    data_y=data_diffusivity_katz_h[:, 1] * htm.ureg.cm**2 * htm.ureg.s**-1,
    source=katz_src,
    isotope="H",
)


data_diffusivity_katz_d = data_diffusivity_katz[2:, 2:4].astype(float)
katz_diffusivity_copper_d = Diffusivity(
    data_T=1000 / data_diffusivity_katz_d[:, 0] * htm.ureg.K,
    data_y=data_diffusivity_katz_d[:, 1] * htm.ureg.cm**2 * htm.ureg.s**-1,
    source=katz_src,
    isotope="D",
)


data_diffusivity_katz_t = data_diffusivity_katz[2:, 4:].astype(float)
katz_diffusivity_copper_t = Diffusivity(
    data_T=1000 / data_diffusivity_katz_t[:, 0] * htm.ureg.K,
    data_y=data_diffusivity_katz_t[:, 1] * htm.ureg.cm**2 * htm.ureg.s**-1,
    source=katz_src,
    isotope="T",
)

# ################# Eichenauer 1957 #############################
eichenauer_diffusivity_copper_h = Diffusivity(
    1.1e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.4 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(700 * htm.ureg.K, 920 * htm.ureg.K),
    source="eichenauer_notitle_1957",
    isotope="H",
)

eichenauer_solubility_copper_h = Solubility(
    S_0=4.9e23 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.37 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(700 * htm.ureg.K, 920 * htm.ureg.K),
    source="eichenauer_notitle_1957",
    isotope="H",
)

# ################# Perkins 1973 #############################
perkins_diffusivity_copper_h = Diffusivity(
    1.06e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.4 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(410 * htm.ureg.K, 710 * htm.ureg.K),
    source="perkins_permeation_1973",
    isotope="H",
)

# ################# Tanabe 1987 #############################
tanabe_diffusivity_copper_d = Diffusivity(
    6.7e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.24 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(298 * htm.ureg.K, 1070 * htm.ureg.K),
    source="tanabe_hydrogen_1987",
    isotope="D",
    note="from Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials",
)

# ################# Eichenauer 1965 #############################
eichenauer_diffusivity_copper_d = Diffusivity(
    6.19e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.392 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(703 * htm.ureg.K, 913 * htm.ureg.K),
    source="eichenauer_notitle_1965",
    isotope="D",
)

eichenauer_solubility_copper_d = Solubility(
    S_0=3.19e24 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.41 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(703 * htm.ureg.K, 913 * htm.ureg.K),
    source="eichenauer_notitle_1965",
    isotope="D",
)

# ################# Anderl 1990 #############################
anderl_diffusivity_copper_d = Diffusivity(
    9.26e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.409 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(638 * htm.ureg.K, 723 * htm.ureg.K),
    source="anderl_hydrogen_1990",
    isotope="D",
)


# ################# Anderl 1999 #############################
anderl_diffusivity_copper_d_1999 = Diffusivity(
    2.1e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.52 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(700 * htm.ureg.K, 800 * htm.ureg.K),
    source="anderl_deuterium_1999",
    isotope="D",
)


# ################# Sakamoto 1982 #############################
sakamoto_diffusivity_copper_h = Diffusivity(
    3.69e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    36820 * htm.ureg.J * htm.ureg.mol**-1,
    range=(292 * htm.ureg.K, 339 * htm.ureg.K),
    source="sakamoto_electrochemical_1982",
    isotope="H",
)

# ################# Otsuka 2010 #############################
otsuka_diffusivity_copper_t = Diffusivity(
    1.11e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    0.399 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(303 * htm.ureg.K, 353 * htm.ureg.K),
    source="otsuka_behavior_2010",
    isotope="T",
)

# ################# Thomas 1967 #############################
thomas_solubility_copper_h = Solubility(
    S_0=1.90e24 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.51 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(770 * htm.ureg.K, 1320 * htm.ureg.K),
    source="thomas_solubility_1967",
    isotope="H",
)

# ################# Wampler 1976 #############################
wampler_solubility_copper_h = Solubility(
    S_0=1.07e24 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.44 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(770 * htm.ureg.K, 1070 * htm.ureg.K),
    source="wampler_precipitation_1976",
    isotope="H",
)

data_T_mclellan = (
    np.array(
        [
            1027.0,
            1005.0,
            939.0,
            911.0,
            871.0,
            846.0,
            809.0,
            778.0,
            755.0,
            723.0,
            659.0,
            609.0,
            594.0,
        ]
    )
    * htm.ureg.degC
)  # in degC (see Table 1)

data_y_mclellan = (
    np.array(
        [
            7.20,
            7.17,
            4.88,
            4.21,
            3.55,
            3.10,
            2.33,
            2.33,
            1.90,
            1.54,
            0.931,
            0.698,
            0.552,
        ]
    )
    * 1e-5
)  # in at.fr Pa-1/2 see Table 1
data_y_mclellan *= (
    1 / COPPER_MOLAR_VOLUME * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5
)  # in mol H m-3 Pa-1/2


mclellan_solubility = Solubility(
    data_T=data_T_mclellan,
    data_y=data_y_mclellan,
    isotope="H",
    source="mclellan_solid_1973",
)

anderl_recombination = RecombinationCoeff(
    pre_exp=9.1e-18 * htm.ureg.m**4 * htm.ureg.s**-1 * htm.ureg.particle**-1,
    act_energy=0.99 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    source="anderl_deuterium_1999",
)


houben_permeability = Permeability(
    pre_exp=3e-6
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.mbar**-0.5,
    act_energy=77 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="houben_comparison_2022",
    isotope="D",
)

properties = [
    reiter_diffusivity_copper,
    magnusson_diffusivity_copper,
    katz_diffusivity_copper_h,
    katz_diffusivity_copper_d,
    katz_diffusivity_copper_t,
    eichenauer_diffusivity_copper_h,
    perkins_diffusivity_copper_h,
    tanabe_diffusivity_copper_d,
    eichenauer_diffusivity_copper_d,
    anderl_diffusivity_copper_d,
    anderl_diffusivity_copper_d_1999,
    sakamoto_diffusivity_copper_h,
    otsuka_diffusivity_copper_t,
    reiter_solubility_copper,
    eichenauer_solubility_copper_d,
    thomas_solubility_copper_h,
    wampler_solubility_copper_h,
    eichenauer_solubility_copper_h,
    mclellan_solubility,
    anderl_recombination,
    houben_permeability,
]

for prop in properties:
    prop.material = htm.COPPER

htm.database += properties
