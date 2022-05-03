from h_transport_materials.materials import Material
from h_transport_materials.property import ArheniusProperty

frauenfelder_src = "R. Frauenfelder. 'Solution and Diffusion of Hydrogen in Tungsten'. In: Journal of Vacuum Science and Technology 6.3 (May 1969), pp. 388–397. doi: 10.1116/1.1492699."
frauenfelder_diffusivity = ArheniusProperty(pre_exp=2.4e-7, act_energy=0.39, source=frauenfelder_src, name="Frauenfelder (1969)")
frauenfelder_solubility = ArheniusProperty(pre_exp=1.87e24, act_energy=1.04, source=frauenfelder_src, name="Frauenfelder (1969)")


reiter_src = "Reiter, F., Forcey, K. S. & Gervasini, G. A Compilation of Tritium: Material Interaction Parameters in Fusion Reactor Materials (Publications Office of the European Union, Luxembourg, 1996)"
reiter_diffusivity_tungsten = ArheniusProperty(pre_exp=1.9e-7, act_energy=0.2, source=reiter_src, name="Reiter (1996)")


tungsten = Material(D=frauenfelder_diffusivity, S=frauenfelder_solubility, name="tungsten")

