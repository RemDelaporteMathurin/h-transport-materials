from h_transport_materials.property import ArrheniusProperty, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb
from h_transport_materials import diffusivities, solubilities


def kJ_per_mol_to_eV(E):
    E_in_J = E * 1000
    return E_in_J * k_B / Rg  # eV


alire_diffusivity = ArrheniusProperty(
    pre_exp=13.0e-4,
    act_energy=kJ_per_mol_to_eV(
        150.0
    ),  # TODO check Shimada paper for inconsistency with original paper
    range=(898, 1178),
    # source=frauenfelder_src,
    name="Alire (1976)",
    isotope="H",
    author="alire",
    year=1976,
)


lithium_diffusivities = [alire_diffusivity]

lithium_solubilities = []

for prop in lithium_diffusivities + lithium_solubilities:
    prop.material = "lithium"

diffusivities.properties += lithium_diffusivities
solubilities.properties += lithium_solubilities
