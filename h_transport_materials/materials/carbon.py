import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


causey_diffusivity = Diffusivity(
    D_0=0.93e-4,
    E_D=2.8,
    range=(900, 1473),
    source="causey_interaction_1989",
    isotope="H",
)

atsumi_diffusivity = Diffusivity(
    D_0=1.69 * 1e-4,
    E_D=c.kJ_per_mol_to_eV(251),
    range=(500 + 273.15, 900 + 273.15),
    isotope="D",
    source="atsumi_absorption_1988",
    note="Equation 5 of Atsumi's paper",
)

atsumi_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.9e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(-19.2),
    source="atsumi_absorption_1988",
    isotope="H",
)

properties = [causey_diffusivity, atsumi_diffusivity, atsumi_solubility]

for prop in properties:
    prop.material = "carbon"

htm.database += properties
