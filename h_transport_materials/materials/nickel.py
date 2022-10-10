import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

NI_MOLAR_VOLUME = 6.59e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/nickel

volkl_diffusivity = Diffusivity(
    D_0=6.87e-7,
    E_D=c.kJ_per_mol_to_eV(40.5),
    range=(300, 1473),
    isotope="H",
    source="volkl_5_1975",
)

robertson_diffusivity = Diffusivity(
    D_0=3.72e-7,
    E_D=c.kJ_per_mol_to_eV(40.2),
    range=(273, 1673),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    isotope="H",
    year=1973,
)

louthan_diffusivity_H = Diffusivity(
    D_0=7.0e-7,
    E_D=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="H",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_D = Diffusivity(
    D_0=7.0e-7 / 2**0.5,
    E_D=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="D",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_T = Diffusivity(
    D_0=7.0e-7 / 3**0.5,
    E_D=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="T",
    source="louthan_hydrogen_1975",
)

robertson_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.52e-6 * htm.avogadro_nb / NI_MOLAR_VOLUME,
    E_S=c.kJ_per_mol_to_eV(12.5),
    range=(273, 1673),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    year=1973,
    isotope="H",
)


louthan_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.5e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(15.8),
    range=(300, 500),
    isotope="H",
    source="louthan_hydrogen_1975",
)


properties = [
    volkl_diffusivity,
    robertson_diffusivity,
    louthan_diffusivity_H,
    louthan_diffusivity_D,
    louthan_diffusivity_T,
    robertson_solubility,
    louthan_solubility,
]

for prop in properties:
    prop.material = "nickel"

htm.database += properties
