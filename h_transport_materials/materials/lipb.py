from h_transport_materials.materials import Material
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb

molar_mass_li = 0.06941  # kg/mol
molar_mass_Pb = 0.2072  # kg/mol
# For Pb-16Li
molar_mass_lipb = molar_mass_Pb + 16 * molar_mass_li
rho_lipb = 10163.197  # kg/m3  at 300K
atom_density_lipb = (rho_lipb * avogadro_nb) / molar_mass_lipb

eg_src = "E. g, DOI:111"
eg_diffusivity = ArrheniusProperty(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
)
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


wu_src = "C.H. Wu, DOI:10.1016/0022-3115(83)90069-7"
eg_solubility = Solubility(
    pre_exp=6.33e-07 * atom_density_lipb,
    act_energy=0,
    range=(850, 1040),
    source=wu_src,
    name="Wu (1983)",
    author="wu",
    year=1983,
    isotope="D",
    units="m-3 Pa-1/2",
)


chan_src = "Y.C. Chan, E.Veleckis, DOI:10.1016/0022-3115(84)90198-3"
chan_solubility = Solubility(
    pre_exp=4.7e-07 * atom_density_lipb,
    act_energy=9000 * k_B / Rg,
    range=(573, 773),
    source=chan_src,
    name="Chan (1984)",
    author="chan",
    year=1984,
    isotope="H",
    units="m-3 Pa-1/2",
)


katsuta_src = "H. Katsuta, H. Iwamoto, H. Ohno, DOI:10.1016/0022-3115(85)90127-8"
katsuta_solubility = Solubility(
    pre_exp=1.08e-06 * atom_density_lipb,
    act_energy=0,
    range=(573, 723),
    source=katsuta_src,
    name="Katsuta (1985)",
    author="katsuta",
    year=1985,
    isotope="H",
    units="m-3 Pa-1/2",
)


fauvet_src = "P. Fauvet, J. Sannier, DOI:10.1016/0022-3115(88)90301-7"
fauvet_solubility = Solubility(
    pre_exp=2.7e-08 * atom_density_lipb,
    act_energy=0,
    range=(722, 724),
    source=fauvet_src,
    name="Fauvet (1988)",
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
    name="Schumacher (1990)",
    author="schumacher",
    year=1990,
    isotope="H",
    units="m-3 Pa-1/2",
)


eg_src = "E. g, DOI:111"
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


eg_src = "E. g, DOI:111"
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


eg_src = "E. g, DOI:111"
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


eg_src = "E. g, DOI:111"
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


eg_src = "E. g, DOI:111"
eg_solubility = Solubility(
    pre_exp=1,
    act_energy=0,
    range=(1, 1),
    source=eg_src,
    name="eg (0000)",
    author="eg",
    year=0000,
    isotope="H",
    units="m-3 Pa-1/2",
)


tungsten_diffusivities = [
    frauenfelder_diffusivity,
    liu_diffusivity_tungsten,
    heinola_diffusivity_tungsten,
    johnson_diffusivity_tungsten_h,
    johnson_diffusivity_tungsten_t,
    moore_diffusivity_tungsten_t,
    zakharov_diffusivity_tungsten_h,
    ryabchikov_diffusivity_tungsten_h,
    esteban_diffusivity_tungsten_h,
    esteban_diffusivity_tungsten_d,
    esteban_diffusivity_tungsten_t,
    holzner_diffusivity_tungsten_h,
    holzner_diffusivity_tungsten_d,
    fernandez_diffusivity_tungsten_h,
]

tungsten_solubilities = [
    frauenfelder_solubility,
    esteban_solubility_tungsten_h,
    esteban_solubility_tungsten_d,
    esteban_solubility_tungsten_t,
]

for prop in tungsten_diffusivities + tungsten_solubilities:
    prop.material = "tungsten"

diffusivities.properties += tungsten_diffusivities
solubilities.properties += tungsten_solubilities
