from h_transport_materials import diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb

atm_to_Pa = 101325  # Pa/atm


def atm05_to_pa05(P):
    return P * atm_to_Pa**0.5


molar_mass_li = 0.06941  # kg/mol
molar_mass_Pb = 0.2072  # kg/mol
# For Pb-16Li
molar_mass_lipb = molar_mass_Pb + 16 * molar_mass_li
rho_lipb = 10163.197  # kg/m3  at 300K
atom_density_lipb = (rho_lipb * avogadro_nb) / molar_mass_lipb


wu_src = "C.H. Wu, DOI:10.1016/0022-3115(83)90069-7"
wu_solubility = Solubility(
    pre_exp=6.33e-07 * atom_density_lipb,
    act_energy=0,
    range=(850, 1040),
    source=wu_src,
    name="D Wu (1983)",
    author="wu",
    year=1983,
    isotope="D",
    units="m-3 Pa-1/2",
)


# extrapolated to Pb-17Li
chan_src = "Y.C. Chan, E.Veleckis, DOI:10.1016/0022-3115(84)90198-3"
chan_solubility = Solubility(
    pre_exp=4.7e-07 * atom_density_lipb,
    act_energy=9000 * k_B / Rg,
    range=(573, 773),
    source=chan_src,
    name="H Chan (1984)",
    author="chan",
    year=1984,
    isotope="H",
    units="m-3 Pa-1/2",
)


katsuta_src = "H. Katsuta, H. Iwamoto, H. Ohno, DOI:10.1016/0022-3115(85)90127-8"
pre_exp_katsuta = 2.9e3  # atm^0.5  / at.fr.
pre_exp_katsuta = atm05_to_pa05(pre_exp_katsuta)  # Pa^0.5 / at.fr.
pre_exp_katsuta = 1 / pre_exp_katsuta  # at.fr. / Pa^0.5

katsuta_solubility = Solubility(
    pre_exp=pre_exp_katsuta * atom_density_lipb,
    act_energy=0,
    range=(573, 723),
    source=katsuta_src,
    name="H Katsuta (1985)",
    author="katsuta",
    year=1985,
    isotope="H",
    units="m-3 Pa-1/2",
)


fauvet_src = "P. Fauvet, J. Sannier, DOI:10.1016/0022-3115(88)90301-7"
fauvet_diffusivity = ArrheniusProperty(
    pre_exp=1.5e-09,
    act_energy=0,
    range=(722, 724),  # TODO should be 723 link to issue #37
    source=fauvet_src,
    name="H Fauvet (1988)",
    author="fauvet",
    year=1988,
    isotope="H",
)
fauvet_solubility = Solubility(
    pre_exp=2.7e-08 * atom_density_lipb,
    act_energy=0,
    range=(722, 724),  # TODO should be 723 link to issue #37
    source=fauvet_src,
    name="H Fauvet (1988)",
    author="fauvet",
    year=1988,
    isotope="H",
    units="m-3 Pa-1/2",
)


schumacher_src = "R. Schumacher, A. Weiss, DOI:10.1002/bbpc.19900940612"
schumacher_solubility = Solubility(
    pre_exp=8.98e-07 * atom_density_lipb,
    act_energy=6100 * k_B / Rg,
    range=(508, 1040),
    source=schumacher_src,
    name="H Schumacher (1990)",
    author="schumacher",
    year=1990,
    isotope="H",
    units="m-3 Pa-1/2",
)


reiter_src = "F. Reiter, DOI:10.1016/0920-3796(91)90003-9"
reiter_diffusivity_h = ArrheniusProperty(
    pre_exp=4.03e-08,
    act_energy=19500 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="H Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="H",
)
reiter_diffusivity_d = ArrheniusProperty(
    pre_exp=4.03e-08,
    act_energy=19500 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="D Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="D",
)
reiter_diffusivity_t = ArrheniusProperty(
    pre_exp=4.03e-08,
    act_energy=19500 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="T Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="T",
)
reiter_solubility_h = Solubility(
    pre_exp=2.44e-08 * atom_density_lipb,
    act_energy=1350 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="H Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="H",
    units="m-3 Pa-1/2",
)
reiter_solubility_d = Solubility(
    pre_exp=2.36e-08 * atom_density_lipb,
    act_energy=1350 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="D Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="D",
    units="m-3 Pa-1/2",
)
reiter_solubility_t = Solubility(
    pre_exp=2.32e-08 * atom_density_lipb,
    act_energy=1350 * k_B / Rg,
    range=(508, 700),
    source=reiter_src,
    name="T Reiter (1991)",
    author="reiter",
    year=1991,
    isotope="T",
    units="m-3 Pa-1/2",
)


aiello_src = (
    "A. Aiello, A. Ciampichetti, G. Benamati, DOI:10.1016/j.fusengdes.2005.06.364"
)
aiello_solubility = Solubility(
    pre_exp=4.66e-06 * atom_density_lipb,
    act_energy=13399 * k_B / Rg,
    range=(600, 900),
    source=aiello_src,
    name="H Aiello (2006)",
    author="aiello",
    year=2006,
    isotope="H",
    units="m-3 Pa-1/2",
)


shibuya_src = (
    "Y. Shibuya, M. Aida, Y.Fujii, M. Okamoto, DOI:10.1016/0022-3115(87)90006-7"
)
shibuya_diffusivity = ArrheniusProperty(
    pre_exp=2.62e-03,
    act_energy=6630 * k_B / Rg,
    range=(573, 773),
    source=shibuya_src,
    name="T Shibuya (1987)",
    author="shibuya",
    year=1987,
    isotope="T",
)


terai_src = (
    "T. Terai, S. Nagai, T. Yoneoka, Y. Takashi, DOI:10.1016/0022-3115(92)90504-E"
)
terai_diffusivity = ArrheniusProperty(
    pre_exp=2.50e-07,
    act_energy=27000 * k_B / Rg,
    range=(573, 973),
    source=terai_src,
    name="T Terai (1987)",
    author="terai",
    year=1987,
    isotope="T",
)

alberro_src = "G. Alberro, I. Penalva, F. Legarda, G.A. Esteban, DOI:10.1016/j.fusengdes.2015.05.060"
alberro_solubility = Solubility(
    pre_exp=8.64e-3 * avogadro_nb,
    act_energy=9000 * k_B / Rg,
    range=(523, 922),
    source=alberro_src,
    name="H Alberro (2015)",
    author="alberro",
    year=2015,
    isotope="H",
    units="m-3 Pa-1/2",
)


lipb_diffusivities = [
    fauvet_diffusivity,
    reiter_diffusivity_h,
    reiter_diffusivity_d,
    reiter_diffusivity_t,
    shibuya_diffusivity,
    terai_diffusivity,
]

lipb_solubilities = [
    wu_solubility,
    chan_solubility,
    katsuta_solubility,
    fauvet_solubility,
    schumacher_solubility,
    reiter_solubility_h,
    reiter_solubility_d,
    reiter_solubility_t,
    aiello_solubility,
    alberro_solubility,
]

for prop in lipb_diffusivities + lipb_solubilities:
    prop.material = "lipb"

diffusivities.properties += lipb_diffusivities
solubilities.properties += lipb_solubilities
