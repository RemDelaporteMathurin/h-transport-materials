import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

causey_diffusivity = Diffusivity(
    D_0=0.93e-4 * u.m**2 * u.s**-1,
    E_D=2.8 * u.eV * u.particle**-1,
    range=(900 * u.K, 1473 * u.K),
    source="causey_interaction_1989",
    isotope="H",
)

atsumi_diffusivity = Diffusivity(
    D_0=1.69 * u.cm**2 * u.s**-1,
    E_D=251 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(500, u.degC),
        u.Quantity(900, u.degC),
    ),
    isotope="D",
    source="atsumi_absorption_1988",
    note="Equation 5 of Atsumi's paper",
)

atsumi_solubility = Solubility(
    S_0=1.9e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-19.2 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(850, u.degC),
        u.Quantity(1050, u.degC),
    ),
    source="atsumi_absorption_1988",
    isotope="H",
)

data_T_petucci_graphite = [
    90.0,
    100.0,
    110.0,
    125.0,
    150.0,
    175.0,
    200.0,
    250.0,
    300.0,
    350.0,
    400.0,
    450.0,
    500.0,
    550.0,
    600.0,
    650.0,
    700.0,
] * u.K
data_y_petucci_graphite = (
    [
        2.16,
        2.97,
        3.16,
        3.56,
        4.08,
        6.10,
        10.95,
        16.96,
        25.76,
        33.61,
        38.41,
        43.77,
        60.75,
        69.45,
        82.01,
        86.16,
        89.95,
    ]
    * u.angstrom**2
    * u.ps**-1
)

petucci_diffusivity_graphite = Diffusivity(
    data_T=data_T_petucci_graphite,
    data_y=data_y_petucci_graphite,
    source="petucci_diffusion_2013",
    isotope="H",
    note="H2 diffusion in graphite calculated by molecular dynamics. Data from table III",
)


data_T_petucci_graphene = [40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0] * u.K
data_y_petucci_graphene = (
    [175.71, 385.92, 490.17, 656.99, 789.03, 849.91, 1082.79] * u.angstrom**2 * u.ps**-1
)
petucci_diffusivity_graphene = Diffusivity(
    data_T=data_T_petucci_graphene,
    data_y=data_y_petucci_graphene,
    source="petucci_diffusion_2013",
    isotope="H",
    note="H2 diffusion in graphene calculated by molecular dynamics. Data from table III",
)

import numpy as np

graphite_density = 2.266 * u.g / u.cm**3

carbon_atomic_mass = 12.011 * u.g / u.mol

graphite_atomic_density = graphite_density / carbon_atomic_mass

shirasu_solubility_IG_110U = Solubility(
    S_0=np.exp(-14.5) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-18.2 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite IG-110U, data from Table 1",
    range=(u.Quantity(700, u.degC), u.Quantity(1000, u.degC)),
    isotope="H",
)

shirasu_solubility_POCO_AXS_5Q = Solubility(
    S_0=np.exp(-15.6) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-21.5 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite POCO AXS-5Q, data from Table 1",
    range=(u.Quantity(700, u.degC), u.Quantity(1000, u.degC)),
    isotope="H",
)

shirasu_solubility_ISO_880U_low_temp = Solubility(
    S_0=np.exp(-15.8) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-22.0 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite ISO-880U, data from Table 1",
    range=(u.Quantity(700, u.degC), u.Quantity(900, u.degC)),
    isotope="H",
)

shirasu_solubility_ISO_880U_high_temp = Solubility(
    S_0=np.exp(-18.5) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-48.2 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite ISO-880U, data from Table 1",
    range=(u.Quantity(900, u.degC), u.Quantity(1000, u.degC)),
    isotope="H",
)

shirasu_solubility_EK_98_low_temp = Solubility(
    S_0=np.exp(-14.7) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-13.5 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite EK-98, data from Table 1",
    range=(u.Quantity(700, u.degC), u.Quantity(800, u.degC)),
    isotope="H",
)

shirasu_solubility_EK_98_high_temp = Solubility(
    S_0=np.exp(-18.5) * graphite_atomic_density * u.Pa**-0.5,
    E_S=-47.6 * u.kJ / u.mol,
    source="shirasu_thermodynamic_1993",
    note="graphite EK-98, data from Table 1",
    range=(u.Quantity(800, u.degC), u.Quantity(1000, u.degC)),
    isotope="H",
)

properties = [
    causey_diffusivity,
    atsumi_diffusivity,
    atsumi_solubility,
    petucci_diffusivity_graphite,
    petucci_diffusivity_graphene,
    shirasu_solubility_IG_110U,
    shirasu_solubility_POCO_AXS_5Q,
    shirasu_solubility_ISO_880U_low_temp,
    shirasu_solubility_ISO_880U_high_temp,
    shirasu_solubility_EK_98_low_temp,
    shirasu_solubility_EK_98_high_temp,
]

for prop in properties:
    prop.material = htm.CARBON

htm.database += properties
