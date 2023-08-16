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

properties = [causey_diffusivity, atsumi_diffusivity, atsumi_solubility]

for prop in properties:
    prop.material = htm.CARBON

htm.database += properties
