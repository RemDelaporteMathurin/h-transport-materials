import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
from h_transport_materials.property import RecombinationCoeff
import numpy as np

u = htm.ureg

abramov_diffusivity = Diffusivity(
    D_0=8.0e-9 * u.m**2 * u.s**-1,
    E_D=35.1 * u.kJ * u.mol**-1,
    range=(620 * u.K, 775 * u.K),
    isotope="D",
    source="abramov_deuterium_1990",
)


shapovalov_solubility = Solubility(
    isotope="H",
    S_0=1.90e-2 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=16.8 * u.kJ * u.mol**-1,
    range=(673 * u.K, 1473 * u.K),
    author="shapovalov",
    source="Shapovalov, V.I., Dukel'skii, Y.M., 1988. Izv. Akad. Nauk SSR Met. 5, 201–203",
    year=1988,
    note="couldn't find the original paper so took values from Shimada 2020 review",
)

jones_diffusivity = Diffusivity(
    isotope="T",
    D_0=np.exp(-6.53) * u.cm**2 * u.s**-1,
    E_D=965 * u.K * htm.k_B,
    range=(400 * u.K, 900 * u.K),
    source="jones_hydrogen_1967",
    note="Jones also gives a solubility but the units are weird",
)

dolan_recombination = RecombinationCoeff(
    pre_exp=1.46e-29 * u.m**4 * u.s**-1 * u.particle**-1,
    act_energy=0.214 * u.eV * u.particle**-1,
    range=(333 * u.K, 800 * u.K),
    source="dolan_assessment_1994",
    isotope="H",
    note="Comes from a review (p. 14). The data from Hsu 1990 https://doi.org/10.1016/0022-3115(90)90049-S (range taking from them) seems to have been used by the PERI code to extract D/2kr then using D from another source Dolan obtained Kr.",
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
