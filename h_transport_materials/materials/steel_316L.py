import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability
import h_transport_materials.conversion as c
from h_transport_materials.materials.iron import IRON_MOLAR_VOLUME


reiter_diffusivity = Diffusivity(
    D_0=3.70e-7,
    E_D=c.kJ_per_mol_to_eV(51.9),
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 10 papers on diffusivity from Reiter compilation review",
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.8e-6 * htm.avogadro_nb / IRON_MOLAR_VOLUME,
    E_S=c.kJ_per_mol_to_eV(13.1),
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 5 papers on diffusivity from Reiter compilation review",
)

houben_pre_exp = 8e-7  # mol/ (m s mbar^0.5)
houben_pre_exp *= htm.avogadro_nb  # / (m s mbar^0.5)
houben_pre_exp *= (1e-3) ** 0.5  # / (m s bar^0.5)
houben_pre_exp = htm.conversion.barn_to_Pan(houben_pre_exp, -0.5)  # / (m s Pa^0.5)

houben_permeability = Permeability(
    pre_exp=houben_pre_exp,
    act_energy=htm.conversion.kJ_per_mol_to_eV(58),
    source="houben_comparison_2022",
    isotope="D",
)


properties = [reiter_diffusivity, reiter_solubility, houben_permeability]

for prop in properties:
    prop.material = "steel_316l"

htm.database += properties
