from h_transport_materials.materials import Material
from h_transport_materials import diffusivities, solubilities
from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb

frauenfelder_src = "R. Frauenfelder. 'Solution and Diffusion of Hydrogen in Tungsten'. In: Journal of Vacuum Science and Technology 6.3 (May 1969), pp. 388–397. doi: 10.1116/1.1492699."
frauenfelder_diffusivity = ArrheniusProperty(
    pre_exp=2.4e-7,
    act_energy=0.39,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    author="frauenfelder",
    year=1969,
    isotope="H",
)
frauenfelder_solubility = Solubility(
    pre_exp=1.87e24,
    act_energy=1.04,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
    author="frauenfelder",
    year=1969,
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
