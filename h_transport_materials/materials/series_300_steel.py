import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


perng_diffusivity = Diffusivity(
    D_0=2.01e-7,
    E_D=c.kJ_per_mol_to_eV(49.3),
    range=(373, 623),
    source="perng_effects_1986",
    isotope="H",
    note="best fit for 4 different austenitic steels",
)

perng_solubility = Solubility(
    units="m-3 Pa-1/2",
    range=(373, 623),
    S_0=2.70e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(6.9),
    isotope="H",
    source="perng_effects_1986",
)

properties = [perng_diffusivity, perng_solubility]

for prop in properties:
    prop.material = "300_series_steel"

htm.database += properties
