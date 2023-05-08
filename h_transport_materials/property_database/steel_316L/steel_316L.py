import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)
from h_transport_materials.property_database.iron import IRON_MOLAR_VOLUME
import numpy as np

u = htm.ureg

reiter_diffusivity = Diffusivity(
    D_0=3.70e-7 * u.m**2 * u.s**-1,
    E_D=51.9 * u.kJ * u.mol**-1,
    range=(500 * u.K, 1200 * u.K),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 10 papers on diffusivity from Reiter compilation review",
)

reiter_solubility = Solubility(
    S_0=5.8e-6 / IRON_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=13.1 * u.kJ * u.mol**-1,
    range=(500 * u.K, 1200 * u.K),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 5 papers on diffusivity from Reiter compilation review",
)

houben_permeability = Permeability(
    pre_exp=8e-7 * u.mol * u.m**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=58 * u.kJ * u.mol**-1,
    source="houben_comparison_2022",
    isotope="D",
)

kishimoto_permeability = Permeability(
    pre_exp=7.1e3 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.MPa**-0.5,
    act_energy=0.69 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_diffusivity = Diffusivity(
    D_0=1.3e-2 * u.cm**2 * u.s**-1,
    E_D=0.52 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=16 * u.ccNTP * u.cm**-3 * u.MPa**-0.5,
    E_S=0.13 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

esteban_dissociation_coeff_clean = DissociationCoeff(
    pre_exp=1.6e-3 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=48.2 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

esteban_recombination_coeff_clean = RecombinationCoeff(
    pre_exp=6.8e-3 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=20.4 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="clean surface, stationary",
)

esteban_dissociation_coeff_oxidised = DissociationCoeff(
    pre_exp=1.3e-6 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=68.9 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="oxidised surface, stationary",
)

esteban_recombination_coeff_oxidised = RecombinationCoeff(
    pre_exp=5.5e-6 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=41.2 * u.kJ * u.mol**-1,
    isotope="T",
    range=(450 * u.K, 620 * u.K),
    source="perujo_low_1996",
    note="oxidised surface, stationary",
)

# TODO fit Forcey data ourselves
forcey_permeability = Permeability(
    pre_exp=1.80e-7 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=64030 * u.J * u.mol**-1,
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
)

forcey_diffusivity = Diffusivity(
    D_0=3.82e-7 * u.m**2 * u.s**-1,
    E_D=45500 * u.J * u.mol**-1,
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
)

forcey_solubility = Solubility(
    S_0=1.50 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=18510 * u.J * u.mol**-1,
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
)

xiukui_permeability = Permeability(
    pre_exp=3.90e-4 * u.mol * u.m**-1 * u.s**-1 * u.MPa**-0.5,
    act_energy=64.06 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(200, u.degC),
        u.Quantity(430, u.degC),
    ),
    isotope="H",
    source="xiukui_hydrogen_1989",
)

xiukui_diffusivity = Diffusivity(
    D_0=4.79e-7 * u.m**2 * u.s**-1,
    E_D=51.59 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(200, u.degC),
        u.Quantity(430, u.degC),
    ),
    isotope="H",
    source="xiukui_hydrogen_1989",
)

lee_permeability_data = np.genfromtxt(
    htm.absolute_path("lee_2011/permeability.csv"),
    delimiter=",",
    names=True,
)
lee_data_invT = lee_permeability_data["X"] * u.K**-1
lee_permeability = Permeability(
    data_T=1 / lee_data_invT,
    data_y=lee_permeability_data["Y"] * u.mol * u.s**-1 * u.m**-1 * u.Pa**-0.5,
    isotope="H",
    source="lee_hydrogen_2011",
)

lee_diffsol_data = np.genfromtxt(
    htm.absolute_path("lee_2011/diffusivity_solubility.csv"),
    delimiter=",",
    names=True,
)
lee_data_invT = lee_diffsol_data["diffusivityX"] * u.K**-1
lee_diffusivity = Diffusivity(
    data_T=1 / lee_data_invT,
    data_y=lee_diffsol_data["diffusivityY"] * u.m**2 * u.s**-1,
    isotope="H",
    source="lee_hydrogen_2011",
)
lee_data_invT = lee_diffsol_data["solubilityX"] * u.K**-1
lee_solubility = Solubility(
    data_T=1 / lee_data_invT,
    data_y=lee_diffsol_data["solubilityY"] * u.mol * u.m**-3 * u.Pa**-0.5,
    isotope="H",
    source="lee_hydrogen_2011",
)

serra_data = np.genfromtxt(
    htm.absolute_path("serra_2005/data.csv"),
    delimiter=",",
    names=True,
)

serra_permeability = Permeability(
    data_T=1 / serra_data["permx"] * u.K,
    data_y=serra_data["permy"] * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_diffusivity = Diffusivity(
    data_T=1 / serra_data["diffx"] * u.K,
    data_y=serra_data["diffy"] * u.m**2 * u.s**-1,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_solubility = Solubility(
    data_T=1 / serra_data["solx"] * u.K,
    data_y=serra_data["soly"] * u.mol * u.m**-3 * u.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)

properties = [
    reiter_diffusivity,
    reiter_solubility,
    houben_permeability,
    kishimoto_permeability,
    kishimoto_diffusivity,
    kishimoto_solubility,
    esteban_dissociation_coeff_clean,
    esteban_recombination_coeff_clean,
    esteban_dissociation_coeff_oxidised,
    esteban_recombination_coeff_oxidised,
    forcey_permeability,
    forcey_diffusivity,
    forcey_solubility,
    xiukui_permeability,
    xiukui_diffusivity,
    lee_permeability,
    lee_diffusivity,
    lee_solubility,
    serra_permeability,
    serra_diffusivity,
    serra_solubility,
]

for prop in properties:
    prop.material = htm.STEEL_316L

htm.database += properties
