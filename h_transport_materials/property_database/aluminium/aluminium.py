import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability
import numpy as np

u = htm.ureg

# Fig 6 of Young's paper
data_diffusivity_young = np.genfromtxt(
    htm.absolute_path("young_diffusivity.csv"),
    delimiter=",",
)

young_diffusivity = Diffusivity(
    data_T=1e3 / data_diffusivity_young[:, 0] * u.K,
    data_y=np.exp(data_diffusivity_young[:, 1]) * u.cm**2 * u.s**-1,
    isotope="H",
    source="young_diffusion_1998",
)

ransley_solubility = Solubility(
    isotope="H",
    S_0=2.32e-2 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=39.7 * u.kJ * u.mol**-1,
    range=(723 * u.K, 873 * u.K),
    author="ransley",
    year=1948,
    source="Ransley, C.E., Neufeld, H., 1948. J. Inst. Met. 74, 599–620",
)

eichenauer_permeability = Permeability(
    pre_exp=0.38e-5 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=18900 * u.K * htm.k_B,
    range=(630 * u.K, 870 * u.K),
    isotope="H",
    source="eichenauer_notitle_1961",
    note="could not find the original paper, found in DOI:10.2172/5277693",
)

# TODO find a way to verify the conversion
cochran_permeability = Permeability(
    pre_exp=0.45e-5 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=12360 * u.K * htm.k_B,
    range=(670 * u.K, 870 * u.K),
    isotope="H",
    source="cochran_permeability_1961",
    note="the units given in the original paper are odd. This is the conversion found in DOI:10.2172/5277693",
)

# TODO fit this
song_permeability = Permeability(
    pre_exp=1e-6 * u.mol * u.m**-1 * u.s**-1 * u.MPa**-0.5,
    act_energy=52.5 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(400, u.degC),
        u.Quantity(500, u.degC),
    ),
    isotope="H",
    source="song_study_1997",
    note="natural oxide",
)

saitoh_diffusivity = Diffusivity(
    D_0=6.1e-5 * u.m**2 * u.s**-1,
    E_D=54.8 * u.kJ * u.mol**-1,
    range=(446 * u.K, 681 * u.K),
    isotope="H",
    source="saitoh_hydrogen_1994",
)

hashimoto_diffusivity = Diffusivity(
    D_0=0.26 * u.cm**2 * u.s**-1,
    E_D=0.62 * u.eV * u.particle**-1,
    range=(
        u.Quantity(300, u.degC),
        u.Quantity(400, u.degC),
    ),
    isotope="H",
    source="hashimoto_hydrogen_1983",
)

ichimura_diffusivity = Diffusivity(
    D_0=4.58e-6 * u.m**2 * u.s**-1,
    E_D=37.0 * u.kJ * u.mol**-1,
    isotope="H",
    range=(573 * u.K, 923 * u.K),
    source="ichimura_grain_1991",
    note="columnar grain",
)

outlaw_diffusivity = Diffusivity(
    data_T=u.Quantity([450, 475, 500, 525, 550, 575, 600, 625], u.degC),
    data_y=[3.14e-9, 4.12e-9, 5.30e-9, 6.72e-9, 8.38e-9, 1.03e-8, 1.26e-8, 1.52e-8]
    * u.m**2
    * u.s**-1,
    isotope="H",
    source="outlaw_diffusion_1982",
)

# TODO fit this ourselves (table 2)
ishikawa_diffusivity = Diffusivity(
    D_0=9.2e-5 * u.m**2 * u.s**-1,
    E_D=55.25 * u.kJ * u.mol**-1,
    range=(285 * u.K, 328 * u.K),
    isotope="H",
    source="ishikawa_diffusivity_1986",
)

properties = [
    young_diffusivity,
    ransley_solubility,
    eichenauer_permeability,
    cochran_permeability,
    song_permeability,
    saitoh_diffusivity,
    hashimoto_diffusivity,
    ichimura_diffusivity,
    outlaw_diffusivity,
    ishikawa_diffusivity,
]

for prop in properties:
    prop.material = htm.ALUMINIUM

htm.database += properties
