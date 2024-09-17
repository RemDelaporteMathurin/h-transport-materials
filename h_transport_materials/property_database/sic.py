import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

causey_alpha_diffusivity = Diffusivity(
    D_0=1.09e-2 * u.cm**2 * u.s**-1,
    E_D=54.9 * u.kcal * u.mol**-1,
    note="alpha-SiC single crystal",
    range=(u.Quantity(800, u.degC), u.Quantity(1400, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

causey_beta_diffusivity = Diffusivity(
    D_0=28e-2 * u.cm**2 * u.s**-1,
    E_D=65.0 * u.kcal * u.mol**-1,
    note="beta-SiC single crystal",
    range=(u.Quantity(800, u.degC), u.Quantity(1000, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

causey_al_doped_alpha_diffusivity = Diffusivity(
    D_0=4.04e-4 * u.cm**2 * u.s**-1,
    E_D=34.0 * u.kcal * u.mol**-1,
    note="Al-doped alpha-SiC single crystal",
    range=(u.Quantity(500, u.degC), u.Quantity(900, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

causey_vapor_dep_beta_diffusivity = Diffusivity(
    D_0=1.58e-4 * u.cm**2 * u.s**-1,
    E_D=73.6 * u.kcal * u.mol**-1,
    note="vapor-deposited beta-SiC",
    range=(u.Quantity(1000, u.degC), u.Quantity(1300, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

causey_hot_pressed_alpha_diffusivity = Diffusivity(
    D_0=0.904e-4 * u.cm**2 * u.s**-1,
    E_D=48.2 * u.kcal * u.mol**-1,
    note="hot-pressed alpha-SiC",
    range=(u.Quantity(500, u.degC), u.Quantity(800, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

causey_sintered_beta_diffusivity = Diffusivity(
    D_0=8.54e-4 * u.cm**2 * u.s**-1,
    E_D=64.2 * u.kcal * u.mol**-1,
    note="sintered beta-SiC",
    range=(u.Quantity(800, u.degC), u.Quantity(1100, u.degC)),
    source="causey_hydrogen_1978",
    isotope="T",
)

sic_density = (
    3.21 * u.g * u.cm**-3
)  # ref: https://pubchem.ncbi.nlm.nih.gov/compound/Silicon-carbide
sic_molecular_weight = (
    40.096 * u.g * u.mol**-1
)  # ref: https://pubchem.ncbi.nlm.nih.gov/compound/Silicon-carbide
sic_atom_density = sic_density / sic_molecular_weight


causey_beta_vapor_dep_solubility = Solubility(
    S_0=8.77e-9 * u.atm**-0.5 * sic_atom_density,
    E_S=-37.0 * u.kcal * u.mol**-1,
    range=(u.Quantity(1000, u.degC), u.Quantity(1400, u.degC)),
    note="vapor-deposited beta-SiC, at 1 atm",
    isotope="D",
    source="causey_hydrogen_1978",
)

properties = [
    causey_alpha_diffusivity,
    causey_beta_diffusivity,
    causey_al_doped_alpha_diffusivity,
    causey_vapor_dep_beta_diffusivity,
    causey_hot_pressed_alpha_diffusivity,
    causey_sintered_beta_diffusivity,
    causey_beta_vapor_dep_solubility,
]

for prop in properties:
    prop.material = htm.SIC

htm.database += properties
