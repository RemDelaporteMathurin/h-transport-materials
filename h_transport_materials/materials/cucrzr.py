from h_transport_materials.materials import Material
from h_transport_materials.property import ArheniusProperty

anderl_src = "R. A. Anderl et al. 'Deuterium transport in Cu, CuCrZr, and Cu/Be'. In: Journal of Nuclear Materials 266-269 (Mar. 1999), pp. 761–765"
anderl_recombination = ArheniusProperty(pre_exp=2.9e-14, act_energy=1.92, source=anderl_src, name="Anderl (1999)")

serra_src = "E Serra and A Perujo. 'Hydrogen and deuterium transport and inventory parameters in a Cu–0.65Cr–0.08Zr alloy for fusion reactor applications'. en. In: Journal of Nuclear Materials 258-263 (Oct. 1998), pp. 1028–1032"
serra_diffusivity = ArheniusProperty(pre_exp=3.9e-7, act_energy=0.42, source=serra_src, name="Serra (1998)")
serra_solubility = ArheniusProperty(pre_exp=4.28e23, act_energy=0.39, source=serra_src, name="Serra (1998)")


cucrzr = Material(D=serra_diffusivity, S=serra_solubility, name="cucrzr")
