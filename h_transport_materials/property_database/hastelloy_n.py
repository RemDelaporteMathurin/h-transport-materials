import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

u = htm.ureg

webb_permeability = Permeability(
    pre_exp=190 * u.ccSTP * u.mm * u.cm**-2 * u.h**-1 * u.atm**-0.5,
    act_energy=13800 * u.cal * u.mol**-1,
    isotope="H",
    range=(1 / 0.0015 * u.K, 1 / 0.0014 * u.K),
    source="webb_permeation_1965",
    note="Table 1",
)


# TODO fit these ourselves
zhang_permeability_h = Permeability(
    pre_exp=2.5e-7 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=60.27 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="H",
    source="zhang_diffusion_2020",
)

zhang_permeability_d = Permeability(
    pre_exp=1.9e-7 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=60.61 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="D",
    source="zhang_diffusion_2020",
)

zhang_diffusivity_h = Diffusivity(
    D_0=7.0e-7 * u.m**2 * u.s**-1,
    E_D=44.11 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="H",
    source="zhang_diffusion_2020",
)

zhang_diffusivity_d = Diffusivity(
    D_0=6.1e-7 * u.m**2 * u.s**-1,
    E_D=43.70 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="D",
    source="zhang_diffusion_2020",
)

zhang_solubility_h = Solubility(
    S_0=0.36e-7 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=17.60 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="H",
    source="zhang_diffusion_2020",
)

zhang_solubility_d = Solubility(
    S_0=0.31e-7 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=17.81 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(800, u.degC)),
    isotope="D",
    source="zhang_diffusion_2020",
)

properties = [
    webb_permeability,
    zhang_permeability_h,
    zhang_permeability_d,
    zhang_diffusivity_h,
    zhang_diffusivity_d,
    zhang_solubility_h,
    zhang_solubility_d,
]

for prop in properties:
    prop.material = htm.HASTELLOY_N

htm.database += properties
