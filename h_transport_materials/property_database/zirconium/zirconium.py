import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

import numpy as np
from pathlib import Path


ZIRCONIUM_MOLAR_VOLUME = 1.4e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/zirconium

kearns_diffusivity = Diffusivity(
    D_0=7.73e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=10.830 * htm.ureg.kcal * htm.ureg.mol**-1,
    range=(548 * htm.ureg.K, 973 * htm.ureg.K),
    isotope="H",
    source="kearns_diffusion_1972",
)

hsu_diffusivity = Diffusivity(
    D_0=2.7e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=24.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="T",
    source="hsu_palladium-catalyzed_1986",
)

kearns_solubility = Solubility(
    S_0=4.30e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=-49.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    source="kearns_terminal_1967",
    range=(602 * htm.ureg.K, 1069 * htm.ureg.K),
    note="this was found in Shimada 2020 review 'Tritium Transport in Fusion Reactor Materials'"
    + "however, I can't find this activation energy in Kearns paper",
)

yamanaka_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/yamanaka_1989/solubility.csv",
    delimiter=",",
)

yamanaka_solubility = Solubility(
    data_T=1e4 / yamanaka_solubility_data[:, 0] * htm.ureg.K,
    data_y=np.exp(yamanaka_solubility_data[:, 1])
    / ZIRCONIUM_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    source="yamanaka_effect_1989",
    isotope="H",
)

properties = [
    kearns_diffusivity,
    hsu_diffusivity,
    kearns_solubility,
    yamanaka_solubility,
]

for prop in properties:
    prop.material = htm.ZIRCONIUM

htm.database += properties
