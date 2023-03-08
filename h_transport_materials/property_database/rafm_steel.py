import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility


causey_diffusivity = Diffusivity(
    D_0=1.00e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=13.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 973 * htm.ureg.K),
    source="causey_416_2012",
    isotope="H",
    note="value obtained from a average estimate from several authors",
)

causey_solubility = Solubility(
    S_0=4.40e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=28.6 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 973 * htm.ureg.K),
    isotope="H",
    source="causey_416_2012",
    note="value obtained from a average estimate from several authors",
)

forcey_diffusivity = htm.Diffusivity(
    D_0=7.17e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=13490 * htm.ureg.J * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(250, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

forcey_solubility = htm.Solubility(
    S_0=1.29
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,  # NOTE: typo in Eq. 16
    E_S=29620 * htm.ureg.J * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(250, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

# TODO fit this ourselves
serra_diffusivity_f82h = htm.Diffusivity(
    D_0=1.07e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=13950 * htm.ureg.J * htm.ureg.mol**-1,
    range=(373 * htm.ureg.K, 743 * htm.ureg.K),
    source="serra_influence_1997",
    isotope="D",
)
serra_solubility_f82h = htm.Solubility(
    S_0=0.377 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=26880 * htm.ureg.J * htm.ureg.mol**-1,
    range=(373 * htm.ureg.K, 743 * htm.ureg.K),
    source="serra_influence_1997",
    isotope="D",
    note="F82H",
)


# TODO fit this ourselves
serra_diffusivity_batman = htm.Diffusivity(
    D_0=1.9e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=15190 * htm.ureg.J * htm.ureg.mol**-1,
    range=(373 * htm.ureg.K, 743 * htm.ureg.K),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)
serra_solubility_batman = htm.Solubility(
    S_0=0.198 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=24703 * htm.ureg.J * htm.ureg.mol**-1,
    range=(373 * htm.ureg.K, 743 * htm.ureg.K),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)

# TODO: try and fit this ourselves (Figures 10 and 11)
pisarev_diffusivity = htm.Diffusivity(
    D_0=8.6e-4 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.075 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(573 * htm.ureg.K, 873 * htm.ureg.K),
    isotope="D",
    source="pisarev_surface_2001",
    note="F82H",
)

pisarev_solubility = htm.Solubility(
    S_0=2.0e18 * htm.ureg.particle * htm.ureg.cm**-3 * htm.ureg.Pa**-0.5,
    E_S=0.343 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(573 * htm.ureg.K, 873 * htm.ureg.K),
    isotope="D",
    source="pisarev_surface_2001",
)


# TODO: fit this ourselves from the paper
esteban_diffusivity_h = htm.Diffusivity(
    D_0=5.489e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=10574 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="H",
    source="esteban_tritium_2000",
    note="OPTIFER-IVb",
)

esteban_solubility_h = htm.Solubility(
    S_0=0.328 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=29005 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="H",
    source="esteban_tritium_2000",
)

esteban_diffusivity_d = htm.Diffusivity(
    D_0=4.613e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=11321 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="D",
    source="esteban_tritium_2000",
)

esteban_solubility_d = htm.Solubility(
    S_0=0.325 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=28955 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="D",
    source="esteban_tritium_2000",
)


esteban_diffusivity_t = htm.Diffusivity(
    D_0=4.166e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=12027 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

esteban_solubility_t = htm.Solubility(
    S_0=0.271 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=27905 * htm.ureg.J * htm.ureg.mol**-1,
    range=(423 * htm.ureg.K, 892 * htm.ureg.K),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

# TODO fit the data ourselves (Fig 5 and )
# TODO: Dolinski gives permeability and diffusivities, should we compute solubility ourselves?

dolinski_diffusivity_d = htm.Diffusivity(
    D_0=6.6e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=29 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(520 * htm.ureg.K, 900 * htm.ureg.K),
    isotope="D",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)

dolinski_diffusivity_t = htm.Diffusivity(
    D_0=5.0e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=29 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(520 * htm.ureg.K, 900 * htm.ureg.K),
    isotope="T",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)


# TODO: fit this ourselves Figures 2, 3
kulsartov_diffusivity_h = htm.Diffusivity(
    D_0=2.8e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=8.0 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(400, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="H",
    source="kulsartov_investigation_2006",
    note="F85H steel",
)

kulsartov_solubility_h = htm.Solubility(
    S_0=7.7 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=33 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(400, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="H",
    source="kulsartov_investigation_2006",
)


kulsartov_diffusivity_d = htm.Diffusivity(
    D_0=2.3e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=7.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(400, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="D",
    source="kulsartov_investigation_2006",
)
kulsartov_solubility_d = htm.Solubility(
    S_0=7.4 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=36 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(
        htm.ureg.Quantity(400, htm.ureg.degC),
        htm.ureg.Quantity(600, htm.ureg.degC),
    ),
    isotope="D",
    source="kulsartov_investigation_2006",
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
]

for prop in properties:
    prop.material = htm.STEEL_RAFM

htm.database += properties
