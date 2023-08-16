import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import numpy as np

u = htm.ureg

ZIRCONIUM_MOLAR_VOLUME = 1.4e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/zirconium

kearns_diffusivity = Diffusivity(
    D_0=7.73e-3 * u.cm**2 * u.s**-1,
    E_D=10.830 * u.kcal * u.mol**-1,
    range=(548 * u.K, 973 * u.K),
    isotope="H",
    source="kearns_diffusion_1972",
)

kearns_solubility = Solubility(
    S_0=4.30e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-49.5 * u.kJ * u.mol**-1,
    isotope="H",
    source="kearns_terminal_1967",
    range=(602 * u.K, 1069 * u.K),
    note="this was found in Shimada 2020 review 'Tritium Transport in Fusion Reactor Materials'"
    + "however, I can't find this activation energy in Kearns paper",
)

yamanaka_solubility_data = np.genfromtxt(
    htm.absolute_path("yamanaka_1989/solubility.csv"),
    delimiter=",",
)

yamanaka_solubility = Solubility(
    data_T=1e4 / yamanaka_solubility_data[:, 0] * u.K,
    data_y=np.exp(yamanaka_solubility_data[:, 1])
    / ZIRCONIUM_MOLAR_VOLUME
    * u.mol
    * u.m**-3
    * u.Pa**-0.5,
    source="yamanaka_effect_1989",
    isotope="H",
)

properties = [
    kearns_diffusivity,
    kearns_solubility,
    yamanaka_solubility,
]

for prop in properties:
    prop.material = htm.ZIRCONIUM

htm.database += properties
