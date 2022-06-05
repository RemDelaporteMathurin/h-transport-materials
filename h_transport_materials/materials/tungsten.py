from h_transport_materials.materials import Material
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb

frauenfelder_src = "frauenfelder_solution_1969"
frauenfelder_diffusivity = ArrheniusProperty(
    pre_exp=2.4e-7,
    act_energy=0.39,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    isotope="H",
)
frauenfelder_solubility = Solubility(
    pre_exp=1.87e24,
    act_energy=1.04,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    isotope="H",
    units="m-3 Pa-1/2",
)


liu_src = "liu_hydrogen_2014"
liu_diffusivity_tungsten = ArrheniusProperty(
    pre_exp=5.13e-8,
    act_energy=0.21,
    range=(200, 3000),
    source=liu_src,
    name="H Liu (2014)",
    isotope="H",
)


heinola_src = "heinola_diffusion_2010"
heinola_diffusivity_tungsten = ArrheniusProperty(
    pre_exp=5.2e-8,
    act_energy=0.21,
    source=heinola_src,
    name="H Heinola (2010)",
    isotope="H",
)

johnson_src = "johnson_hydrogen_2010"
johnson_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=6.32e-7,
    act_energy=0.39,
    source=johnson_src,
    name="H Johnson (2010)",
    isotope="H",
)

johnson_diffusivity_tungsten_t = ArrheniusProperty(
    pre_exp=5.16e-7,
    act_energy=0.40,
    source=johnson_src,
    name="T Johnson (2010)",
    isotope="T",
)


moore_diffusivity_tungsten_t = ArrheniusProperty(
    pre_exp=7.2e-8,
    act_energy=173.7e3 * k_B / Rg,
    range=(1510, 1902),
    source="moore_adsorptiondesorption_1964",
    name="T Moore (1964)",
    isotope="T",
)


zakharov_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=6.0e-4,
    act_energy=103.4e3 * k_B / Rg,
    range=(400, 1200),
    source="zakharov_hydrogen_1975",
    name="H Zakharov (1973)",
    isotope="H",
)

ryabchikov_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=8.1e-6,
    act_energy=82.9e3 * k_B / Rg,
    range=(1055, 1570),
    source="ryabchikov_notitle_1964",
    name="H Ryabchikov (1964)",
    isotope="H",
)

esteban_src = "esteban_hydrogen_2001"
esteban_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=5.68e-10,
    act_energy=9.3e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
    isotope="H",
)

esteban_diffusivity_tungsten_d = ArrheniusProperty(
    pre_exp=5.49e-10,
    act_energy=10e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
    isotope="D",
)

esteban_diffusivity_tungsten_t = ArrheniusProperty(
    pre_exp=5.34e-10,
    act_energy=11.2e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
    isotope="T",
)


esteban_solubility_tungsten_h = Solubility(
    pre_exp=2.9e-2 * avogadro_nb,
    act_energy=26.9e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
    isotope="H",
    units="m-3 Pa-1/2",
)

esteban_solubility_tungsten_d = Solubility(
    pre_exp=0.75e-2 * avogadro_nb,
    act_energy=28.7e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
    isotope="D",
    units="m-3 Pa-1/2",
)

esteban_solubility_tungsten_t = Solubility(
    pre_exp=2.25e-2 * avogadro_nb,
    act_energy=27.8e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
    isotope="T",
    units="m-3 Pa-1/2",
)

holzner_src = "holzner_solute_2020"
holzner_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=2.06e-3 * 1e-4,
    act_energy=0.28,
    range=(1600, 2600),
    source=holzner_src,
    name="H Holzner (2020)",
    isotope="H",
)
holzner_diffusivity_tungsten_d = ArrheniusProperty(
    pre_exp=1.60e-3 * 1e-4,
    act_energy=0.28,
    range=(1600, 2600),
    source=holzner_src,
    name="D Holzner (2020)",
    isotope="D",
)

fernandez_diffusivity_tungsten_h = ArrheniusProperty(
    pre_exp=1.93e-7,
    act_energy=0.20,
    range=(300, 1200),
    name="H Fernandez (2015)",
    source="fernandez_hydrogen_2015",
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
