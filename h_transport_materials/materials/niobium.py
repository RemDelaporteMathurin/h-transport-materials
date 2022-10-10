import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

NIOBIUM_MOLAR_VOLUME = 1.08e-8  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/niobium

volkl_diffusivity = Diffusivity(
    D_0=5.00e-8,
    E_D=c.kJ_per_mol_to_eV(10.2),
    range=(273, 773),
    source="volkl_5_1975",
    isotope="H",
)

schober_diffusivity = Diffusivity(
    D_0=4.4e-8,
    E_D=c.kJ_per_mol_to_eV(12.8),
    source="schober_h_1990",
    isotope="H",
)

veleckis_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.26e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(-35.3),
    range=(625, 944),
    source="veleckis_thermodynamic_1969",
    isotope="H",
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=3.6e-6 * htm.avogadro_nb / NIOBIUM_MOLAR_VOLUME,
    E_S=c.kJ_per_mol_to_eV(-33.9),
    source="reiter_compilation_1996",
    isotope="H",
)

properties = [
    volkl_diffusivity,
    schober_diffusivity,
    veleckis_solubility,
    reiter_solubility,
]

for prop in properties:
    prop.material = "niobium"

htm.database += properties
