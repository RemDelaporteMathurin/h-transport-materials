import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


TITANIUM_MOLAR_VOLUME = 1.05e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/titanium

reiter_diffusivity = Diffusivity(
    D_0=6.9e-7,
    E_D=c.kJ_per_mol_to_eV(49.1),
    source="reiter_compilation_1996",
    isotope="T",
    range=(873, 1123),
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.06e-5 * htm.avogadro_nb / TITANIUM_MOLAR_VOLUME,
    E_S=c.kJ_per_mol_to_eV(-42.7),
    range=(873, 1123),
    isotope="T",
    source="reiter_compilation_1996",
)

properties = [reiter_diffusivity, reiter_solubility]

for prop in properties:
    prop.material = "titanium"

htm.database += properties
