import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability
import numpy as np

u = htm.ureg

tanabe_diffusivity = Diffusivity(
    D_0=4.00e-8 * u.m**2 * u.s**-1,
    E_D=22.3 * u.kJ * u.mol**-1,
    isotope="H",
    range=(500 * u.K, 1100 * u.K),
    source="tanabe_hydrogen_1992",
)

katsuta_diffusivity = Diffusivity(
    D_0=np.exp(-17.547) * u.m**2 * u.s**-1,
    E_D=1.266e3 * u.K * htm.k_B,
    isotope="H",
    range=(833 * u.K, 1193 * u.K),
    source="katsuta_diffusivity_1982",
)

tanabe_solubility = Solubility(
    S_0=3.3 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=37.4 * u.kJ * u.mol**-1,
    range=(500 * u.K, 1100 * u.K),
    isotope="H",
    source="tanabe_hydrogen_1992",
)

katsuta_solubility = Solubility(
    S_0=np.exp(8.703) * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=7.863e3 * u.K * htm.k_B,
    isotope="H",
    range=(833 * u.K, 1193 * u.K),
    source="katsuta_diffusivity_1982",
)


frauenfelder_p_0 = 7.1e-4 * u.torr * u.liter * u.cm**-1 * u.s**-1 * u.torr**-0.5
frauenfelder_permeability = Permeability(
    pre_exp=frauenfelder_p_0 / (htm.Rg * 300 * u.K),
    act_energy=21.5 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(1050, u.degC),
        u.Quantity(2400, u.degC),
    ),
    source="frauenfelder_permeation_1968",
)

guthrie_permeability = Permeability(
    pre_exp=3.8e-3 * u.ccSTP * u.cm**-1 * u.s**-1 * u.atm**-0.5,
    act_energy=17.4 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(270, u.degC),
        u.Quantity(640, u.degC),
    ),
    source="guthrie_permeation_1974",
    note="Figure 7",
)

properties = [
    tanabe_diffusivity,
    katsuta_diffusivity,
    tanabe_solubility,
    katsuta_solubility,
    frauenfelder_permeability,
    guthrie_permeability
]

for prop in properties:
    prop.material = htm.MOLYBDENUM

htm.database += properties
