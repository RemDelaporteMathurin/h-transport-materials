import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)
import numpy as np

u = htm.ureg

STEEL_316L_DENSITY = (
    8.0 * u.g * u.cm**-3
)  # ref https://doi.org/10.31399/asm.hb.mhde2.9781627081993
STEEL_316L_MOLAR_MASS = 56.52 * u.g * u.mol**-1  # TODO compute it from composition
STEEL_316L_MOLAR_VOLUME = STEEL_316L_DENSITY / STEEL_316L_MOLAR_MASS


reiter_diffusivity = Diffusivity(
    D_0=3.70e-7 * u.m**2 * u.s**-1,
    E_D=51.9 * u.kJ * u.mol**-1,
    range=(500 * u.K, 1200 * u.K),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 10 papers on diffusivity from Reiter compilation review",
)

reiter_solubility = Solubility(
    S_0=5.8e-6 * u.Pa**-0.5 * STEEL_316L_MOLAR_VOLUME,
    E_S=13.1 * u.kJ * u.mol**-1,
    range=(500 * u.K, 1200 * u.K),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 5 papers on diffusivity from Reiter compilation review",
)

# TODO fit this ourselves
reiter_1985_solubility_h = Solubility(
    S_0=1.84e-6 * u.Pa**-0.5 * STEEL_316L_MOLAR_VOLUME,
    E_S=6880 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="h",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_solubility_d = Solubility(
    S_0=1.96e-6 * u.Pa**-0.5 * STEEL_316L_MOLAR_VOLUME,
    E_S=8090 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="d",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_diffusivity_h = Diffusivity(
    D_0=2.99e-6 * u.m**2 * u.s**-1,
    E_D=59700 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="h",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_diffusivity_d = Diffusivity(
    D_0=1.74e-6 * u.m**2 * u.s**-1,
    E_D=58100 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="d",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_permeability_h = reiter_1985_diffusivity_h * reiter_1985_solubility_h
reiter_1985_permeability_h.range = reiter_1985_diffusivity_h.range
reiter_1985_permeability_h.isotope = reiter_1985_diffusivity_h.isotope
reiter_1985_permeability_h.source = reiter_1985_diffusivity_h.source
reiter_1985_permeability_h.note = "calculated in HTM"


reiter_1985_permeability_d = reiter_1985_diffusivity_d * reiter_1985_solubility_d
reiter_1985_permeability_d.range = reiter_1985_diffusivity_d.range
reiter_1985_permeability_d.isotope = reiter_1985_diffusivity_d.isotope
reiter_1985_permeability_d.source = reiter_1985_diffusivity_d.source
reiter_1985_permeability_d.note = "calculated in HTM"


# TODO fit this ourselves
reiter_1985_solubility_h = Solubility(
    S_0=1.84e-6 * u.Pa**-0.5 * STEEL_316L_MOLAR_VOLUME,
    E_S=6880 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="h",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_solubility_d = Solubility(
    S_0=1.96e-6 * u.Pa**-0.5 * STEEL_316L_MOLAR_VOLUME,
    E_S=8090 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="d",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_diffusivity_h = Diffusivity(
    D_0=2.99e-6 * u.m**2 * u.s**-1,
    E_D=59700 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="h",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_diffusivity_d = Diffusivity(
    D_0=1.74e-6 * u.m**2 * u.s**-1,
    E_D=58100 * u.J * u.mol**-1,
    range=(600 * u.K, 900 * u.K),
    isotope="d",
    source="reiter_interaction_1985",
    note="probably a unit mistake in the activation energies in original paper",
)

reiter_1985_permeability_h = reiter_1985_diffusivity_h * reiter_1985_solubility_h
reiter_1985_permeability_h.range = reiter_1985_diffusivity_h.range
reiter_1985_permeability_h.isotope = reiter_1985_diffusivity_h.isotope
reiter_1985_permeability_h.source = reiter_1985_diffusivity_h.source
reiter_1985_permeability_h.note = "calculated in HTM"


reiter_1985_permeability_d = reiter_1985_diffusivity_d * reiter_1985_solubility_d
reiter_1985_permeability_d.range = reiter_1985_diffusivity_d.range
reiter_1985_permeability_d.isotope = reiter_1985_diffusivity_d.isotope
reiter_1985_permeability_d.source = reiter_1985_diffusivity_d.source
reiter_1985_permeability_d.note = "calculated in HTM"


houben_permeability_2022 = Permeability(
    pre_exp=8e-7 * u.mol * u.m**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=58 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(300, u.degC),
        u.Quantity(550, u.degC),
    ),
    source="houben_comparison_2022",
    isotope="D",
)

houben_diffusivity_2019 = Diffusivity(
    D_0=6e-7 * u.m**2 * u.s**-1,
    E_D=51 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(500, u.degC)),
    isotope="d",
    source="houben_comparison_2019",
)

houben_permeability_2019 = Permeability(
    pre_exp=8e-7 * u.mol * u.m**-1 * u.ms**-1 * u.mbar**-0.5,
    act_energy=58 * u.kJ * u.mol**-1,
    range=(u.Quantity(300, u.degC), u.Quantity(550, u.degC)),
    isotope="d",
    source="houben_comparison_2019",
)

houben_permeability_2019_rough = Permeability(
    pre_exp=7e-7 * u.mol * u.m**-1 * u.ms**-1 * u.mbar**-0.5,
    act_energy=63 * u.kJ * u.mol**-1,
    range=(u.Quantity(300, u.degC), u.Quantity(550, u.degC)),
    isotope="d",
    source="houben_comparison_2019",
    note="rough",
)

houben_solubility_2019 = Solubility(
    S_0=1 * u.mol * u.m**-3 * u.mbar**-0.5,
    E_S=7 * u.kJ * u.mol**-1,
    range=(u.Quantity(400, u.degC), u.Quantity(500, u.degC)),
    isotope="d",
    source="houben_comparison_2019",
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


shan_permeability_h = Permeability(
    data_T=[500.0, 550.0, 600.0, 650.0, 700.0, 723.0] * u.K,
    data_y=[8.95e-11, 3.46e-10, 1.07e-9, 2.78e-9, 6.30e-9, 8.84e-9]
    * u.mol
    * u.m**-1
    * u.s**-1
    * u.MPa**-0.5,
    isotope="h",
    source="shan_behavior_1991",
    note="Table 1",
)

shan_permeability_t = Permeability(
    data_T=[500.0, 550.0, 600.0, 650.0, 700.0, 723.0] * u.K,
    data_y=[1.72e-11, 6.39e-11, 1.91e-10, 4.82e-10, 1.07e-9, 1.48e-9]
    * u.mol
    * u.m**-1
    * u.s**-1
    * u.MPa**-0.5,
    isotope="t",
    source="shan_behavior_1991",
    note="Table 1",
)

shan_diffusivity_h = Diffusivity(
    data_T=[500.0, 550.0, 600.0, 650.0, 700.0, 723.0] * u.K,
    data_y=[1.39e-12, 4.51e-12, 1.20e-11, 2.76e-11, 5.64e-11, 7.57e-11]
    * u.m**2
    * u.s**-1,
    isotope="h",
    source="shan_behavior_1991",
    note="Table 1",
)

shan_diffusivity_t = Diffusivity(
    data_T=[500.0, 550.0, 600.0, 650.0, 700.0, 723.0] * u.K,
    data_y=[6.00e-12, 8.35e-12, 1.10e-11, 1.39e-11, 1.70e-11, 1.84e-11]
    * u.m**2
    * u.s**-1,
    isotope="t",
    source="shan_behavior_1991",
    note="Table 1",
)

shan_solubility_h = Solubility(
    S_0=shan_permeability_h.pre_exp / shan_diffusivity_h.pre_exp,
    E_S=shan_permeability_h.act_energy - shan_diffusivity_h.act_energy,
    range=shan_permeability_h.range,
    isotope="h",
    source="shan_behavior_1991",
    note="calculated in HTM",
)


shan_solubility_t = Solubility(
    S_0=shan_permeability_t.pre_exp / shan_diffusivity_t.pre_exp,
    E_S=shan_permeability_t.act_energy - shan_diffusivity_t.act_energy,
    range=shan_permeability_t.range,
    isotope="t",
    source="shan_behavior_1991",
    note="calculated in HTM",
)

penzhorn_diffusivity_1 = Diffusivity(
    D_0=1.9e-2 * u.cm**2 * u.s**-1,
    E_D=61300 * u.J * u.mol**-1,
    range=(373.0, 473.0) * u.K,
    isotope="T",
    source="penzhorn_distribution_2010",
    note="Section III.B, temperature range is unclear",
)

penzhorn_diffusivity_2 = Diffusivity(
    D_0=1.5e-2 * u.cm**2 * u.s**-1,
    E_D=57300 * u.J * u.mol**-1,
    range=(373.0, 473.0) * u.K,
    isotope="T",
    source="penzhorn_distribution_2010",
    note="Section III.C, temperature range is unclear",
)

properties = [
    reiter_diffusivity,
    reiter_solubility,
    houben_permeability_2022,
    houben_diffusivity_2019,
    houben_solubility_2019,
    houben_permeability_2019,
    houben_permeability_2019_rough,
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
    reiter_1985_solubility_h,
    reiter_1985_solubility_d,
    reiter_1985_diffusivity_h,
    reiter_1985_diffusivity_d,
    reiter_1985_permeability_h,
    reiter_1985_permeability_d,
    shan_permeability_h,
    shan_permeability_t,
    shan_diffusivity_h,
    shan_diffusivity_t,
    shan_solubility_h,
    shan_solubility_t,
    penzhorn_diffusivity_1,
    penzhorn_diffusivity_2,
]

for prop in properties:
    prop.material = htm.STEEL_316L

htm.database += properties
