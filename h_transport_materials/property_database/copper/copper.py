import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    Permeability,
    RecombinationCoeff,
    Solubility,
)
import numpy as np

u = htm.ureg

COPPER_MOLAR_VOLUME = 7.11e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/copper

# ################# REITER 1996 #############################

reiter_diffusivity_copper = Diffusivity(
    D_0=6.6e-7 * u.m**2 * u.s**-1,
    E_D=0.39 * u.eV * u.particle**-1,
    range=(470 * u.K, 1200 * u.K),
    source="reiter_compilation_1996",
    isotope="T",
)
reiter_solubility_copper = Solubility(
    S_0=3.14e24 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.57 * u.eV * u.particle**-1,
    range=(470 * u.K, 1200 * u.K),
    source="reiter_compilation_1996",
    isotope="T",
)

# copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility_copper, name="copper")


magnusson_diffusivity_copper = Diffusivity(
    D_0=1.74e-6 * u.m**2 * u.s**-1,
    E_D=42000 * u.J * u.mol**-1,
    range=(298 * u.K, 1273 * u.K),
    source="magnusson_self-diffusion_2013",
    isotope="H",
)


# ################# KATZ 1971 #############################

katz_src = "katz_diffusion_1971"
data_diffusivity_katz = htm.structure_data_from_wpd("katz_1971_diffusivity.csv")

katz_diffusivity_copper_h = Diffusivity(
    data_T=1000 / data_diffusivity_katz["h"]["x"] * u.K,
    data_y=data_diffusivity_katz["h"]["y"] * u.cm**2 * u.s**-1,
    source=katz_src,
    isotope="H",
)


katz_diffusivity_copper_d = Diffusivity(
    data_T=1000 / data_diffusivity_katz["d"]["x"] * u.K,
    data_y=data_diffusivity_katz["d"]["y"] * u.cm**2 * u.s**-1,
    source=katz_src,
    isotope="D",
)


katz_diffusivity_copper_t = Diffusivity(
    data_T=1000 / data_diffusivity_katz["t"]["x"] * u.K,
    data_y=data_diffusivity_katz["t"]["y"] * u.cm**2 * u.s**-1,
    source=katz_src,
    isotope="T",
)

# ################# Eichenauer 1957 #############################
eichenauer_diffusivity_copper_h = Diffusivity(
    1.1e-6 * u.m**2 * u.s**-1,
    0.4 * u.eV * u.particle**-1,
    range=(700 * u.K, 920 * u.K),
    source="eichenauer_notitle_1957",
    isotope="H",
)

eichenauer_solubility_copper_h = Solubility(
    S_0=4.9e23 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.37 * u.eV * u.particle**-1,
    range=(700 * u.K, 920 * u.K),
    source="eichenauer_notitle_1957",
    isotope="H",
)

# ################# Perkins 1973 #############################
perkins_diffusivity_copper_h = Diffusivity(
    1.06e-6 * u.m**2 * u.s**-1,
    0.4 * u.eV * u.particle**-1,
    range=(410 * u.K, 710 * u.K),
    source="perkins_permeation_1973",
    isotope="H",
)

# ################# Tanabe 1987 #############################
tanabe_diffusivity_copper_d = Diffusivity(
    6.7e-8 * u.m**2 * u.s**-1,
    0.24 * u.eV * u.particle**-1,
    range=(298 * u.K, 1070 * u.K),
    source="tanabe_hydrogen_1987",
    isotope="D",
    note="from Assessment of Database for Interaction of Tritium with ITER Plasma Facing Materials",
)

# ################# Eichenauer 1965 #############################
eichenauer_diffusivity_copper_d = Diffusivity(
    6.19e-7 * u.m**2 * u.s**-1,
    0.392 * u.eV * u.particle**-1,
    range=(703 * u.K, 913 * u.K),
    source="eichenauer_notitle_1965",
    isotope="D",
)

eichenauer_solubility_copper_d = Solubility(
    S_0=3.19e24 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.41 * u.eV * u.particle**-1,
    range=(703 * u.K, 913 * u.K),
    source="eichenauer_notitle_1965",
    isotope="D",
)

# ################# Anderl 1990 #############################
anderl_diffusivity_copper_d = Diffusivity(
    9.26e-7 * u.m**2 * u.s**-1,
    0.409 * u.eV * u.particle**-1,
    range=(638 * u.K, 723 * u.K),
    source="anderl_hydrogen_1990",
    isotope="D",
)


# ################# Anderl 1999 #############################
anderl_diffusivity_copper_d_1999 = Diffusivity(
    2.1e-6 * u.m**2 * u.s**-1,
    0.52 * u.eV * u.particle**-1,
    range=(700 * u.K, 800 * u.K),
    source="anderl_deuterium_1999",
    isotope="D",
)


# ################# Sakamoto 1982 #############################
sakamoto_diffusivity_copper_h = Diffusivity(
    3.69e-7 * u.m**2 * u.s**-1,
    36820 * u.J * u.mol**-1,
    range=(292 * u.K, 339 * u.K),
    source="sakamoto_electrochemical_1982",
    isotope="H",
)

# ################# Otsuka 2010 #############################
otsuka_diffusivity_copper_t = Diffusivity(
    1.11e-6 * u.m**2 * u.s**-1,
    0.399 * u.eV * u.particle**-1,
    range=(303 * u.K, 353 * u.K),
    source="otsuka_behavior_2010",
    isotope="T",
)

# ################# Thomas 1967 #############################
thomas_solubility_copper_h = Solubility(
    S_0=1.90e24 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.51 * u.eV * u.particle**-1,
    range=(770 * u.K, 1320 * u.K),
    source="thomas_solubility_1967",
    isotope="H",
)

# ################# Wampler 1976 #############################
wampler_solubility_copper_h = Solubility(
    S_0=1.07e24 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.44 * u.eV * u.particle**-1,
    range=(770 * u.K, 1070 * u.K),
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
    * u.degC
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
    1 / COPPER_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5
)  # in mol H m-3 Pa-1/2


mclellan_solubility = Solubility(
    data_T=data_T_mclellan,
    data_y=data_y_mclellan,
    isotope="H",
    source="mclellan_solid_1973",
)

anderl_recombination = RecombinationCoeff(
    pre_exp=9.1e-18 * u.m**4 * u.s**-1 * u.particle**-1,
    act_energy=0.99 * u.eV * u.particle**-1,
    range=(700.0 * u.K, 800.0 * u.K),
    isotope="D",
    source="anderl_deuterium_1999",
)


houben_permeability = Permeability(
    pre_exp=3e-6 * u.mol * u.m**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=77 * u.kJ * u.mol**-1,
    source="houben_comparison_2022",
    range=(u.Quantity(300, u.degC), u.Quantity(550, u.degC)),
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
