from h_transport_materials.materials import Material
from h_transport_materials.property import ArheniusProperty
from h_transport_materials import k_B, Rg, avogadro_nb

frauenfelder_src = "R. Frauenfelder. 'Solution and Diffusion of Hydrogen in Tungsten'. In: Journal of Vacuum Science and Technology 6.3 (May 1969), pp. 388–397. doi: 10.1116/1.1492699."
frauenfelder_diffusivity = ArheniusProperty(
    pre_exp=2.4e-7,
    act_energy=0.39,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
)
frauenfelder_solubility = ArheniusProperty(
    pre_exp=1.87e24,
    act_energy=1.04,
    range=(1100, 2400),
    source=frauenfelder_src,
    name="Frauenfelder (1969)",
)


reiter_src = "Reiter, F., Forcey, K. S. & Gervasini, G. A Compilation of Tritium: Material Interaction Parameters in Fusion Reactor Materials (Publications Office of the European Union, Luxembourg, 1996)"
reiter_diffusivity_tungsten = ArheniusProperty(
    pre_exp=1.9e-7, act_energy=0.2, source=reiter_src, name="Reiter (1996)"
)

liu_src = "Yi-Nan Liu, Hydrogen diffusion in tungsten: A molecular dynamics study, Journal of Nuclear Materials (2014)"
liu_diffusivity_tungsten = ArheniusProperty(
    pre_exp=5.13e-8,
    act_energy=0.21,
    range=(200, 3000),
    source=liu_src,
    name="H Liu (2014)",
)


heinola_src = "K. Heinola, Diffusion of hydrogen in bcc tungsten studied with first principle calculations (2010)"
heinola_diffusivity_tungsten = ArheniusProperty(
    pre_exp=5.2e-8, act_energy=0.21, source=heinola_src, name="H Heinola (2010)"
)

johnson_src = "Hydrogen in tungsten: Absorption, diffusion, vacancy trapping, and decohesion, J. Mater. Res., Vol. 25, No. 2, (2010)"
johnson_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=6.32e-7, act_energy=0.39, source=johnson_src, name="H Johnson (2010)"
)

johnson_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=5.16e-7, act_energy=0.40, source=johnson_src, name="T Johnson (2010)"
)


moore_src = "Close G.E. Moore, F.C. Unterwald J. Chem. Phys., 40 (1964), p. 2639"
moore_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=7.2e-8,
    act_energy=173.7e3 * k_B / Rg,
    range=(1510, 1902),
    source=moore_src,
    name="T Moore (1964)",
)


zakharov_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=6.0e-4,
    act_energy=103.4 * k_B / Rg,
    range=(400, 1200),
    source="Close A.P. Zakharov, V.M. Sharapov, E.I. Evko Sov. Mater. Sci., 9 (1973), p. 149",
    name="H Zakharov (1973)",
)

ryabchikov_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=8.1e-6,
    act_energy=82.9 * k_B / Rg,
    range=(1055, 1570),
    source="L.N. Ryabchikov Ukr. Fiz. Zh., 9 (1964), p. 293",
    name="H Ryabchikov (1964)",
)

esteban_src = "Esteban, Hydrogen isotope diffusive transport parameters in pure polycrystalline tungsten (2001)"
esteban_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=5.68e-10,
    act_energy=9.3e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
)

esteban_diffusivity_tungsten_d = ArheniusProperty(
    pre_exp=5.49e-10,
    act_energy=10e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
)

esteban_diffusivity_tungsten_t = ArheniusProperty(
    pre_exp=5.34e-10,
    act_energy=11.2e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
)


esteban_solubility_tungsten_h = ArheniusProperty(
    pre_exp=2.9e-2 * avogadro_nb,
    act_energy=26.9e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="H Esteban (2001)",
)

esteban_solubility_tungsten_d = ArheniusProperty(
    pre_exp=0.75e-2 * avogadro_nb,
    act_energy=28.7e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="D Esteban (2001)",
)

esteban_solubility_tungsten_t = ArheniusProperty(
    pre_exp=2.25e-2 * avogadro_nb,
    act_energy=27.8e3 * k_B / Rg,
    range=(673, 1073),
    source=esteban_src,
    name="T Esteban (2001)",
)

holzner_src = ": G Holzner et al 2020 Phys. Scr. 2020 014034"
holzner_diffusivity_tungsten_h = ArheniusProperty(
    pre_exp=2.06e-3 * 1e-4,
    act_energy=0.28,
    source=holzner_src,
    name="H Holzner (2020)",
)
holzner_diffusivity_tungsten_d = ArheniusProperty(
    pre_exp=1.60e-3 * 1e-4,
    act_energy=0.28,
    source=holzner_src,
    name="H Holzner (2020)",
)

tungsten = Material(
    D=frauenfelder_diffusivity, S=frauenfelder_solubility, name="tungsten"
)
