import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

NI_MOLAR_VOLUME = 6.59e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/nickel

volkl_diffusivity = ArrheniusProperty(
    pre_exp=6.87e-7,
    act_energy=c.kJ_per_mol_to_eV(40.5),
    range=(300, 1473),
    isotope="H",
    source="volkl_5_1975",
)

robertson_diffusivity = ArrheniusProperty(
    pre_exp=3.72e-7,
    act_energy=c.kJ_per_mol_to_eV(40.2),
    range=(273, 1673),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    year=1973,
)

louthan_diffusivity_H = ArrheniusProperty(
    pre_exp=7.0e-7,
    act_energy=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="H",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_D = ArrheniusProperty(
    pre_exp=7.0e-7 / 2**0.5,
    act_energy=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="D",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_T = ArrheniusProperty(
    pre_exp=7.0e-7 / 3**0.5,
    act_energy=c.kJ_per_mol_to_eV(39.5),
    range=(300, 500),
    isotope="T",
    source="louthan_hydrogen_1975",
)

robertson_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=5.52e-6 * htm.avogadro_nb / NI_MOLAR_VOLUME,
    act_energy=c.kJ_per_mol_to_eV(12.5),
    range=(273, 1673),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    year=1973,
)


louthan_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=5.5e-1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(15.8),
    range=(300, 500),
    isotope="H",
    source="louthan_hydrogen_1975",
)


nickel_diffusivities = [
    volkl_diffusivity,
    robertson_diffusivity,
    louthan_diffusivity_H,
    louthan_diffusivity_D,
    louthan_diffusivity_T,
]

nickel_solubilities = [robertson_solubility, louthan_solubility]

for prop in nickel_diffusivities + nickel_solubilities:
    prop.material = "nickel"

diffusivities.properties += nickel_diffusivities
solubilities.properties += nickel_solubilities
