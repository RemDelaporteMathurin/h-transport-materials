import h_transport_materials as htm

my_D = (
    htm.diffusivities.filter(material="tungsten")
    .filter(author="frauenfelder")
    .filter(year=1969)
)[0]

my_S = (
    htm.solubilities.filter(material="copper")
    # .filter(author="frauenfelder")
    # .filter(isotope="H")
    # .filter(year=1969)
)[0]

my_festim_mat = htm.Material(D=my_D, S=my_S).festim_material
