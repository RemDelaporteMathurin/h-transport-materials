import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability

import numpy as np

tanabe_diffusivity = Diffusivity(
    D_0=4.00e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=22.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(500 * htm.ureg.K, 1100 * htm.ureg.K),
    source="tanabe_hydrogen_1992",
)

katsuta_diffusivity = Diffusivity(
    D_0=np.exp(-17.547) * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=1.266e3 * htm.ureg.K * htm.k_B,
    isotope="H",
    range=(833 * htm.ureg.K, 1193 * htm.ureg.K),
    source="katsuta_diffusivity_1982",
)

tanabe_solubility = Solubility(
    S_0=3.3 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=37.4 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500 * htm.ureg.K, 1100 * htm.ureg.K),
    isotope="H",
    source="tanabe_hydrogen_1992",
)

katsuta_solubility = Solubility(
    S_0=np.exp(8.703) * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=7.863e3 * htm.ureg.K * htm.k_B,
    isotope="H",
    source="katsuta_diffusivity_1982",
)


frauenfelder_p_0 = (
    7.1e-4
    * htm.ureg.torr
    * htm.ureg.liter
    * htm.ureg.cm**-1
    * htm.ureg.s**-1
    * htm.ureg.torr**-0.5
)
frauenfelder_permeability = Permeability(
    pre_exp=frauenfelder_p_0 / (htm.Rg * 300 * htm.ureg.K),
    act_energy=21.5 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(1050, htm.ureg.degC),
        htm.ureg.Quantity(2400, htm.ureg.degC),
    ),
    source="frauenfelder_permeation_1968",
)

properties = [
    tanabe_diffusivity,
    katsuta_diffusivity,
    tanabe_solubility,
    katsuta_solubility,
    frauenfelder_permeability,
]

for prop in properties:
    prop.material = htm.MOLYBDENUM

htm.database += properties
