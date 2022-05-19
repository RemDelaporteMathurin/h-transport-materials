from h_transport_materials.materials import Material
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.property import ArheniusProperty
from h_transport_materials import k_B, Rg, avogadro_nb

frauenfelder_src = "R. Frauenfelder. 'Solution and Diffusion of Hydrogen in Tungsten'. In: Journal of Vacuum Science and Technology 6.3 (May 1969), pp. 388–397. doi: 10.1116/1.1492699."
frauenfelder_diffusivity = ArheniusProperty(
    pre_exp=2.4e-7,
    act_energy=0.39,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    author="frauenfelder",
    year=1969,
    isotope="H",
)
frauenfelder_solubility = ArheniusProperty(
    pre_exp=1.87e24,
    act_energy=1.04,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    author="frauenfelder",
    year=1969,
    isotope="H",
)


liu_src = "Yi-Nan Liu, Hydrogen diffusion in tungsten: A molecular dynamics study, Journal of Nuclear Materials (2014)"
liu_diffusivity_tungsten = ArheniusProperty(
    pre_exp=5.13e-8,
    act_energy=0.21,
    range=(200, 3000),
    source=liu_src,
    year=2014,
    author="liu",
    name="H Liu (2014)",
    isotope="H",
)


heinola_src = "K. Heinola, Diffusion of hydrogen in bcc tungsten studied with first principle calculations (2010)"
heinola_diffusivity_tungsten = ArheniusProperty(
    pre_exp=5.2e-8,
    act_energy=0.21,
    source=heinola_src,
    name="H Heinola (2010)",
    author="heinola",
    year=2010,
    isotope="H",
)

johnson_src = "Hydrogen in tungsten: Absorption, diffusion, vacancy trapping, and decohesion, J. Mater. Res., Vol. 25, No. 2, (2010)"
johnson_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=6.32e-7,
    act_energy=0.39,
    source=johnson_src,
    name="H Johnson (2010)",
    author="johnson",
    year=2010,
    isotope="H",
)

johnson_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=5.16e-7,
    act_energy=0.40,
    source=johnson_src,
    name="T Johnson (2010)",
    author="johnson",
    year=2010,
    isotope="T",
)


moore_src = "Close G.E. Moore, F.C. Unterwald J. Chem. Phys., 40 (1964), p. 2639"
moore_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=7.2e-8,
    act_energy=173.7e3 * k_B / Rg,
    range=(1510, 1902),
    source=moore_src,
    name="T Moore (1964)",
    author="moore",
    year=1964,
    isotope="T",
)


zakharov_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=6.0e-4,
    act_energy=103.4e3 * k_B / Rg,
    range=(400, 1200),
    source="Close A.P. Zakharov, V.M. Sharapov, E.I. Evko Sov. Mater. Sci., 9 (1973), p. 149",
    name="H Zakharov (1973)",
    author="zakharov",
    year=1973,
    isotope="H",
)

ryabchikov_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=8.1e-6,
    act_energy=82.9e3 * k_B / Rg,
    range=(1055, 1570),
    source="L.N. Ryabchikov Ukr. Fiz. Zh., 9 (1964), p. 293",
    name="H Ryabchikov (1964)",
    author="ryabchikov",
    year=1964,
    isotope="H",
)

esteban_src = "Esteban, Hydrogen isotope diffusive transport parameters in pure polycrystalline tungsten (2001)"
esteban_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=5.68e-10,
    act_energy=9.3e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="H",
)

esteban_diffusivity_tungsten_d = ArheniusProperty(
    pre_exp=5.49e-10,
    act_energy=10e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="D",
)

esteban_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=5.34e-10,
    act_energy=11.2e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="T",
)


esteban_solubility_tungsten_h = ArheniusProperty(
    pre_exp=2.9e-2 * avogadro_nb,
    act_energy=26.9e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="H",
)

esteban_solubility_tungsten_d = ArheniusProperty(
    pre_exp=0.75e-2 * avogadro_nb,
    act_energy=28.7e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="D",
)

esteban_solubility_tungsten_t = ArheniusProperty(
    pre_exp=2.25e-2 * avogadro_nb,
    act_energy=27.8e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
    author="esteban",
    year=2001,
    isotope="T",
)

holzner_src = ": G Holzner et al 2020 Phys. Scr. 2020 014034"
holzner_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=2.06e-3 * 1e-4,
    act_energy=0.28,
    range=(1600, 2600),
    source=holzner_src,
    name="H Holzner (2020)",
    author="holzner",
    year=2020,
    isotope="H",
)
holzner_diffusivity_tungsten_d = ArheniusProperty(
    pre_exp=1.60e-3 * 1e-4,
    act_energy=0.28,
    range=(1600, 2600),
    source=holzner_src,
    name="D Holzner (2020)",
    author="holzner",
    year=2020,
    isotope="D",
)

fernandez_src = "N. Fernandez, Y. Ferro, D. Kato 'Hydrogen diffusion and vacancies formation in tungsten: Density Functional Theory calculations and statistical models' Acta Materialia (2015)"
fernandez_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=1.93e-7,
    act_energy=0.20,
    range=(300, 1200),
    name="H Fernandez (2015)",
    author="fernandez",
    year=2015,
    isotope="H",
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

# tungsten = Material(
#     D=frauenfelder_diffusivity, S=frauenfelder_solubility, name="tungsten"
# )
