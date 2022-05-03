from h_transport_materials.property import ArheniusProperty
from h_transport_materials.materials import Material


reiter_src = "F. Reiter, K. S. Forcey, and G. Gervasini. A compilation of tritium : Material interaction parameters in fusion reactor materials. en. Publications Office of the European Union, July 1996."
reiter_diffusivity_copper = ArheniusProperty(pre_exp=6.6e-7, act_energy=0.39, source=reiter_src, name="Reiter (1996)")
reiter_solubility = ArheniusProperty(pre_exp=3.14e24, act_energy=0.57, source=reiter_src, name="Reiter (1996)")

copper = Material(D=reiter_diffusivity_copper, S=reiter_solubility, name="copper")
