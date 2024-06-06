import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

causey_diffusivity = Diffusivity(
    D_0=1.00e-7 * u.m**2 * u.s**-1,
    E_D=13.2 * u.kJ * u.mol**-1,
    range=(300 * u.K, 973 * u.K),
    source="causey_416_2012",
    isotope="H",
    note="value obtained from a average estimate from several authors",
)

causey_solubility = Solubility(
    S_0=4.40e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=28.6 * u.kJ * u.mol**-1,
    range=(300 * u.K, 973 * u.K),
    isotope="H",
    source="causey_416_2012",
    note="value obtained from a average estimate from several authors",
)

forcey_diffusivity = htm.Diffusivity(
    D_0=7.17e-8 * u.m**2 * u.s**-1,
    E_D=13490 * u.J * u.mol**-1,
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

forcey_solubility = htm.Solubility(
    S_0=1.29 * u.mol * u.m**-3 * u.Pa**-0.5,  # NOTE: typo in Eq. 16
    E_S=29620 * u.J * u.mol**-1,
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

# TODO fit this ourselves
serra_diffusivity_f82h = htm.Diffusivity(
    D_0=1.07e-7 * u.m**2 * u.s**-1,
    E_D=13950 * u.J * u.mol**-1,
    range=(373 * u.K, 743 * u.K),
    source="serra_influence_1997",
    isotope="D",
)
serra_solubility_f82h = htm.Solubility(
    S_0=0.377 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=26880 * u.J * u.mol**-1,
    range=(373 * u.K, 743 * u.K),
    source="serra_influence_1997",
    isotope="D",
    note="F82H",
)


# TODO fit this ourselves
serra_diffusivity_batman = htm.Diffusivity(
    D_0=1.9e-7 * u.m**2 * u.s**-1,
    E_D=15190 * u.J * u.mol**-1,
    range=(373 * u.K, 743 * u.K),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)
serra_solubility_batman = htm.Solubility(
    S_0=0.198 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=24703 * u.J * u.mol**-1,
    range=(373 * u.K, 743 * u.K),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)

# TODO: try and fit this ourselves (Figures 10 and 11)
pisarev_diffusivity = htm.Diffusivity(
    D_0=8.6e-4 * u.cm**2 * u.s**-1,
    E_D=0.075 * u.eV * u.particle**-1,
    range=(573 * u.K, 873 * u.K),
    isotope="D",
    source="pisarev_surface_2001",
    note="F82H",
)

pisarev_solubility = htm.Solubility(
    S_0=2.0e18 * u.particle * u.cm**-3 * u.Pa**-0.5,
    E_S=0.343 * u.eV * u.particle**-1,
    range=(573 * u.K, 873 * u.K),
    isotope="D",
    source="pisarev_surface_2001",
)


# TODO: fit this ourselves from the paper
esteban_diffusivity_h = htm.Diffusivity(
    D_0=5.489e-8 * u.m**2 * u.s**-1,
    E_D=10574 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="H",
    source="esteban_tritium_2000",
    note="OPTIFER-IVb",
)

esteban_solubility_h = htm.Solubility(
    S_0=0.328 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=29005 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="H",
    source="esteban_tritium_2000",
)

esteban_diffusivity_d = htm.Diffusivity(
    D_0=4.613e-8 * u.m**2 * u.s**-1,
    E_D=11321 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="D",
    source="esteban_tritium_2000",
)

esteban_solubility_d = htm.Solubility(
    S_0=0.325 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=28955 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="D",
    source="esteban_tritium_2000",
)


esteban_diffusivity_t = htm.Diffusivity(
    D_0=4.166e-8 * u.m**2 * u.s**-1,
    E_D=12027 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

esteban_solubility_t = htm.Solubility(
    S_0=0.271 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=27905 * u.J * u.mol**-1,
    range=(423 * u.K, 892 * u.K),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

# TODO fit the data ourselves (Fig 5 and )
# TODO: Dolinski gives permeability and diffusivities, should we compute solubility ourselves?

dolinski_diffusivity_d = htm.Diffusivity(
    D_0=6.6e-7 * u.m**2 * u.s**-1,
    E_D=29 * u.kJ * u.mol**-1,
    range=(520 * u.K, 900 * u.K),
    isotope="D",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)

dolinski_diffusivity_t = htm.Diffusivity(
    D_0=5.0e-7 * u.m**2 * u.s**-1,
    E_D=29 * u.kJ * u.mol**-1,
    range=(520 * u.K, 900 * u.K),
    isotope="T",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)


# TODO: fit this ourselves Figures 2, 3
kulsartov_diffusivity_h = htm.Diffusivity(
    D_0=2.8e-8 * u.m**2 * u.s**-1,
    E_D=8.0 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(400, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="kulsartov_investigation_2006",
    note="F85H steel",
)

kulsartov_solubility_h = htm.Solubility(
    S_0=7.7 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=33 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(400, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="H",
    source="kulsartov_investigation_2006",
)


kulsartov_diffusivity_d = htm.Diffusivity(
    D_0=2.3e-8 * u.m**2 * u.s**-1,
    E_D=7.8 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(400, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="D",
    source="kulsartov_investigation_2006",
)
kulsartov_solubility_d = htm.Solubility(
    S_0=7.4 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=36 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(400, u.degC),
        u.Quantity(600, u.degC),
    ),
    isotope="D",
    source="kulsartov_investigation_2006",
)


xu_permeability_h = htm.Permeability(
    pre_exp=1.0e-9 * u.mol * u.cm**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=0.46 * u.eV * u.particle**-1,
    range=(u.Quantity(150, u.degC), u.Quantity(500, u.degC)),
    isotope="H",
    source="xu_bi-directional_2017",
    note="Eq 2, F82H",
)

xu_permeability_d = htm.Permeability(
    pre_exp=6.8e-10 * u.mol * u.cm**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=0.46 * u.eV * u.particle**-1,
    range=(u.Quantity(150, u.degC), u.Quantity(500, u.degC)),
    isotope="D",
    source="xu_bi-directional_2017",
    note="Eq 3, F82H",
)

xu_diffusivity_h = htm.Diffusivity(
    D_0=9.9e-4 * u.cm**2 * u.s**-1,
    E_D=0.14 * u.eV * u.particle**-1,
    range=(u.Quantity(250, u.degC), u.Quantity(500, u.degC)),
    isotope="H",
    source="xu_bi-directional_2017",
    note="Eq 5, F82H, effective diffusivity",
)

xu_diffusivity_d = htm.Diffusivity(
    D_0=7.2e-4 * u.cm**2 * u.s**-1,
    E_D=0.14 * u.eV * u.particle**-1,
    range=(u.Quantity(250, u.degC), u.Quantity(500, u.degC)),
    isotope="D",
    source="xu_bi-directional_2017",
    note="Eq 6, F82H, effective diffusivity",
)

xu_solubility_h = htm.Solubility(
    S_0=1.0e-6 * u.mol * u.cm**-3 * u.Pa**-0.5,
    E_S=0.32 * u.eV * u.particle**-1,
    range=(u.Quantity(250, u.degC), u.Quantity(500, u.degC)),
    isotope="H",
    source="xu_bi-directional_2017",
    note="Eq 8, F82H",
)

xu_solubility_d = htm.Solubility(
    S_0=9.4e-7 * u.mol * u.cm**-3 * u.Pa**-0.5,
    E_S=0.32 * u.eV * u.particle**-1,
    range=(u.Quantity(250, u.degC), u.Quantity(500, u.degC)),
    isotope="D",
    source="xu_bi-directional_2017",
    note="Eq 9, F82H",
)

xu_recombination_coeff_d = htm.RecombinationCoeff(
    pre_exp=3.8e-17 * u.particle**-1 * u.cm**4 * u.s**-1,
    act_energy=-0.20 * u.eV * u.particle**-1,
    range=(u.Quantity(250, u.degC), u.Quantity(510, u.degC)),
    isotope="D",
    source="xu_bi-directional_2017",
    note="Eq 11, F82H",
)

properties = [
    causey_diffusivity,
    forcey_diffusivity,
    pisarev_diffusivity,
    esteban_diffusivity_h,
    esteban_diffusivity_d,
    esteban_diffusivity_t,
    dolinski_diffusivity_d,
    dolinski_diffusivity_t,
    kulsartov_diffusivity_h,
    kulsartov_diffusivity_d,
    serra_diffusivity_f82h,
    serra_diffusivity_batman,
    causey_solubility,
    forcey_solubility,
    pisarev_solubility,
    esteban_solubility_h,
    esteban_solubility_d,
    esteban_solubility_t,
    kulsartov_solubility_h,
    kulsartov_solubility_d,
    serra_solubility_f82h,
    serra_solubility_batman,
    xu_permeability_h,
    xu_permeability_d,
    xu_diffusivity_h,
    xu_diffusivity_d,
    xu_solubility_h,
    xu_solubility_d,
    xu_recombination_coeff_d,
]

for prop in properties:
    prop.material = htm.STEEL_RAFM

htm.database += properties
