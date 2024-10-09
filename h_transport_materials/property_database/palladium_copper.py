import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
    Diffusivity,
)
import numpy as np

u = htm.ureg

li_data_T = (
    np.array(
        [
            350,
            375,
            400,
            425,
        ]
    )
    * u.degC
)

li_data_y = (
    np.array(
        [
            1.45e-8,
            1.51e-8,
            1.55e-8,
            1.60e-8,
        ]
    )
    * u.mol
    * u.m**-1
    * u.Pa**-0.5
    * u.s**-1
)

li_permeability_h = Permeability(
    data_T=li_data_T,
    data_y=li_data_y,
    source="li_low_2023",
    isotope="H",
    note="SI Table 1 (supporting information)",
    material=htm.PD52CU,
)

piper_diffusivity_h = Diffusivity(
    D_0=3e-3 * u.cm**2 * u.s**-1,
    E_D=2400 * u.cal * u.mol**-1,
    range=(u.Quantity(50, u.degC), u.Quantity(600, u.degC)),
    isotope="H",
    source="piper_diffusion_2004",
    note="Equation 6 - this Arrhenius fit holds for when the alloy is in the beta phase for 52.5 percent copper. These range values were found outside of the paper.",
    material=htm.PD52CU,
)

onaka_diffusivity = Diffusivity(
    D_0=2.9e-8 * u.m**2 * u.s**-1,
    E_D=0.048 * u.eV * u.particle**-1,
    isotope="D",
    range=(u.Quantity(350, u.K), u.Quantity(600, u.K)),
    source="onaka_characteristic_2016",
    material=htm.PD60CU40,
)

onaka_recombination = htm.RecombinationCoeff(
    pre_exp=1.43e-26 * u.m**4 * u.s**-1 * u.particle**-1,
    act_energy=0.40 * u.eV * u.particle**-1,
    isotope="D",
    range=(u.Quantity(350, u.K), u.Quantity(600, u.K)),
    source="onaka_characteristic_2016",
    material=htm.PD60CU40,
)

properties = [
    li_permeability_h,
    piper_diffusivity_h,
    onaka_recombination,
    onaka_diffusivity,
]


htm.database += properties
