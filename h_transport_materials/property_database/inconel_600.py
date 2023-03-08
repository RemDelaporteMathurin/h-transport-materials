import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)

kishimoto_diffusivity = Diffusivity(
    D_0=4.90e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.44 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    S_0=36 * htm.ureg.ccNTP * htm.ureg.cm**-3 * htm.ureg.MPa**-0.5,
    E_S=0.22 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

kishimoto_permeability = Permeability(
    pre_exp=6.4e3
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.MPa**-0.5,
    act_energy=0.66 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873 * htm.ureg.K, 1173 * htm.ureg.K),
    source="kishimoto_hydrogen_1985",
)

rota_diffusivity_h = Diffusivity(
    D_0=1.7e-2 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=11.9 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_diffusivity_d = Diffusivity(
    D_0=2.0e-2 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=12.4 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_permeability_h = Permeability(
    pre_exp=2.4e15
    * htm.ureg.particle
    * htm.ureg.cm**-1
    * htm.ureg.s**-1
    * htm.ureg.mbar**-0.5,
    act_energy=13.2 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_permeability_d = Permeability(
    pre_exp=2.4e15
    * htm.ureg.particle
    * htm.ureg.cm**-1
    * htm.ureg.s**-1
    * htm.ureg.mbar**-0.5,
    act_energy=13.6 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_solubility_h = Solubility(
    S_0=1.4e17 * htm.ureg.particle * htm.ureg.cm**-3 * htm.ureg.mbar**-0.5,
    E_S=1.3 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_solubility_d = Solubility(
    S_0=1.2e17 * htm.ureg.particle * htm.ureg.cm**-3 * htm.ureg.mbar**-0.5,
    E_S=1.2 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_dissociation_coeff_h = DissociationCoeff(
    pre_exp=2.6e16
    * htm.ureg.particle
    * htm.ureg.cm**-2
    * htm.ureg.s**-1
    * htm.ureg.mbar**-1,
    act_energy=12.7 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_dissociation_coeff_d = DissociationCoeff(
    pre_exp=2.0e15
    * htm.ureg.particle
    * htm.ureg.cm**-2
    * htm.ureg.s**-1
    * htm.ureg.mbar**-1,
    act_energy=11.0 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_recombination_coeff_h = RecombinationCoeff(
    pre_exp=1.3e-18
    * htm.ureg.particle
    * htm.ureg.cm**4
    * htm.ureg.particle**-2
    * htm.ureg.s**-1,
    act_energy=10.1 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

rota_recombination_coeff_d = RecombinationCoeff(
    pre_exp=1.4e-19
    * htm.ureg.particle
    * htm.ureg.cm**4
    * htm.ureg.particle**-2
    * htm.ureg.s**-1,
    act_energy=8.6 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(150, htm.ureg.degC),
        htm.ureg.Quantity(400, htm.ureg.degC),
    ),
    source="rota_measurements_1982",
)

masui_permeability = Permeability(
    pre_exp=2540
    * htm.ureg.ccNTP
    * htm.ureg.mm
    * htm.ureg.cm**-2
    * htm.ureg.h**-1
    * htm.ureg.atm**-0.5,
    act_energy=15800 * htm.ureg.cal * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(800, htm.ureg.degC),
        htm.ureg.Quantity(1000, htm.ureg.degC),
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
