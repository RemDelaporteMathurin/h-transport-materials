import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

import numpy as np

from h_transport_materials.property import RecombinationCoeff

abramov_diffusivity = Diffusivity(
    D_0=8.0e-9 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=35.1 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(620 * htm.ureg.K, 775 * htm.ureg.K),
    isotope="D",
    source="abramov_deuterium_1990",
)


shapovalov_solubility = Solubility(
    isotope="H",
    S_0=1.90e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=16.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1473 * htm.ureg.K),
    author="shapovalov",
    source="Shapovalov, V.I., Dukel'skii, Y.M., 1988. Izv. Akad. Nauk SSR Met. 5, 201–203",
    year=1988,
    note="couldn't find the original paper so took values from Shimada 2020 review",
)

jones_diffusivity = Diffusivity(
    isotope="T",
    D_0=np.exp(-6.53) * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=965 * htm.ureg.K * htm.k_B,
    range=(400 * htm.ureg.K, 900 * htm.ureg.K),
    source="jones_hydrogen_1967",
    note="Jones also gives a solubility but the units are weird",
)

dolan_recombination = RecombinationCoeff(
    pre_exp=1.46e-29 * htm.ureg.m**4 * htm.ureg.s**-1 * htm.ureg.particle**-1,
    act_energy=0.214 * htm.ureg.eV * htm.ureg.particle**-1,
    source="dolan_assessment_1994",
    isotope="H",
)


properties = [
    shapovalov_solubility,
    abramov_diffusivity,
    jones_diffusivity,
    dolan_recombination,
]

for prop in properties:
    prop.material = htm.BERYLLIUM

htm.database += properties
