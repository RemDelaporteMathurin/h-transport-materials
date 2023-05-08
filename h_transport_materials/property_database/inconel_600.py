import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

u = htm.ureg

kishimoto_diffusivity = Diffusivity(
    D_0=4.90e-3 * u.cm**2 * u.s**-1,
    E_D=0.44 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=36 * u.ccNTP * u.cm**-3 * u.MPa**-0.5,
    E_S=0.22 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=6.4e3 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.MPa**-0.5,
    act_energy=0.66 * u.eV * u.particle**-1,
    isotope="H",
    range=(873 * u.K, 1173 * u.K),
    source="kishimoto_hydrogen_1985",
)

rota_diffusivity_h = Diffusivity(
    D_0=1.7e-2 * u.cm**2 * u.s**-1,
    E_D=11.9 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_diffusivity_d = Diffusivity(
    D_0=2.0e-2 * u.cm**2 * u.s**-1,
    E_D=12.4 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_permeability_h = Permeability(
    pre_exp=2.4e15 * u.particle * u.cm**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=13.2 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_permeability_d = Permeability(
    pre_exp=2.4e15 * u.particle * u.cm**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=13.6 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_solubility_h = Solubility(
    S_0=1.4e17 * u.particle * u.cm**-3 * u.mbar**-0.5,
    E_S=1.3 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_solubility_d = Solubility(
    S_0=1.2e17 * u.particle * u.cm**-3 * u.mbar**-0.5,
    E_S=1.2 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_dissociation_coeff_h = DissociationCoeff(
    pre_exp=2.6e16 * u.particle * u.cm**-2 * u.s**-1 * u.mbar**-1,
    act_energy=12.7 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_dissociation_coeff_d = DissociationCoeff(
    pre_exp=2.0e15 * u.particle * u.cm**-2 * u.s**-1 * u.mbar**-1,
    act_energy=11.0 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_recombination_coeff_h = RecombinationCoeff(
    pre_exp=1.3e-18 * u.particle * u.cm**4 * u.particle**-2 * u.s**-1,
    act_energy=10.1 * u.kcal * u.mol**-1,
    isotope="H",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

rota_recombination_coeff_d = RecombinationCoeff(
    pre_exp=1.4e-19 * u.particle * u.cm**4 * u.particle**-2 * u.s**-1,
    act_energy=8.6 * u.kcal * u.mol**-1,
    isotope="D",
    range=(
        u.Quantity(150, u.degC),
        u.Quantity(400, u.degC),
    ),
    source="rota_measurements_1982",
)

masui_permeability = Permeability(
    pre_exp=2540 * u.ccNTP * u.mm * u.cm**-2 * u.h**-1 * u.atm**-0.5,
    act_energy=15800 * u.cal * u.mol**-1,
    range=(
        u.Quantity(800, u.degC),
        u.Quantity(1000, u.degC),
    ),
    isotope="H",
    source="masui_hydrogen_1978",
)

properties = [
    kishimoto_diffusivity,
    kishimoto_solubility,
    kishimoto_permeability,
    rota_diffusivity_h,
    rota_diffusivity_d,
    rota_permeability_h,
    rota_permeability_d,
    rota_solubility_h,
    rota_solubility_d,
    rota_dissociation_coeff_h,
    rota_dissociation_coeff_d,
    rota_recombination_coeff_h,
    rota_recombination_coeff_d,
    masui_permeability,
]

for prop in properties:
    prop.material = htm.INCONEL_600

htm.database += properties
