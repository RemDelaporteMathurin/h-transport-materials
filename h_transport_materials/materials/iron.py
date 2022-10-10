import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

IRON_MOLAR_VOLUME = 7.09e-6  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/iron

volkl_diffusivity = Diffusivity(
    D_0=4.00e-8,
    E_D=c.kJ_per_mol_to_eV(4.5),
    isotope="H",
    range=(573, 1073),
    source="volkl_5_1975",
)

tahara_diffusivity_H = Diffusivity(
    D_0=4.43e-8,
    E_D=c.kJ_per_mol_to_eV(5.3),
    isotope="H",
    range=(500, 1000),
    source="tahara_measurements_1985",
)

tahara_diffusivity_D = Diffusivity(
    D_0=4.28e-8,
    E_D=c.kJ_per_mol_to_eV(6.47),
    isotope="D",
    range=(500, 1000),
    source="tahara_measurements_1985",
)

eichenauer_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.90e-6 / IRON_MOLAR_VOLUME * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(24.3),
    range=(473, 1183),
    isotope="H",
    source="eichenauer_diffusion_1958",
)


properties = [
    volkl_diffusivity,
    tahara_diffusivity_H,
    tahara_diffusivity_D,
    eichenauer_solubility,
]

for prop in properties:
    prop.material = "iron"

htm.database += properties
