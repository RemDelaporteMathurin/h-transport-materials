import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

import numpy as np
from pathlib import Path


ZIRCONIUM_MOLAR_VOLUME = 1.4e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/zirconium

kearns_diffusivity = Diffusivity(
    D_0=7.73e-3 * 1e-4,
    E_D=c.kcal_per_mol_to_eV(10.830),
    range=(548, 973),
    isotope="H",
    source="kearns_diffusion_1972",
)

hsu_diffusivity = Diffusivity(
    D_0=2.7e-8,
    E_D=c.kJ_per_mol_to_eV(24.9),
    isotope="T",
    source="hsu_palladium-catalyzed_1986",
)

kearns_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.30e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(-49.5),
    isotope="H",
    source="kearns_terminal_1967",
    range=(602, 1069),
    note="this was found in Shimada 2020 review 'Tritium Transport in Fusion Reactor Materials'"
    + "however, I can't find this activation energy in Kearns paper",
)

yamanaka_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/yamanaka_1989/solubility.csv",
    delimiter=",",
)

yamanaka_solubility = Solubility(
    units="m-3 Pa-1/2",
    data_T=1e4 / yamanaka_solubility_data[:, 0],
    data_y=np.exp(yamanaka_solubility_data[:, 1])
    * htm.avogadro_nb
    / ZIRCONIUM_MOLAR_VOLUME,
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
    prop.material = "zirconium"

htm.database += properties
