import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


volkl_diffusivity = Diffusivity(
    D_0=4.40e-8,
    E_D=c.kJ_per_mol_to_eV(13.5),
    range=(253, 573),
    isotope="H",
    source="volkl_5_1975",
)

veleckis_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.32e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(-33.7),
    isotope="H",
    range=(623, 904),
    source="veleckis_thermodynamic_1969",
)

properties = [volkl_diffusivity, veleckis_solubility]

for prop in properties:
    prop.material = "tantalum"

htm.database += properties
