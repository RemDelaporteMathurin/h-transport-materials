import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


causey_diffusivity = Diffusivity(
    D_0=1.00e-7,
    E_D=c.kJ_per_mol_to_eV(13.2),
    range=(300, 973),
    source="causey_416_2012",
    isotope="H",
    note="value obtained from a average estimate from several authors",
)

causey_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.40e-1 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(28.6),
    range=(300, 973),
    isotope="H",
    source="causey_416_2012",
    note="value obtained from a average estimate from several authors",
)

forcey_diffusivity = htm.Diffusivity(
    D_0=7.17e-8,
    E_D=c.J_per_mol_to_eV(13490),
    range=(250 + 273.15, 600 + 273.15),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

forcey_solubility = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=1.29 * htm.avogadro_nb,  # NOTE: typo in Eq. 16
    E_S=c.J_per_mol_to_eV(29620),
    range=(250 + 273.15, 600 + 273.15),
    isotope="H",
    source="forcey_hydrogen_1988",
    note="heat-treated reference cast l.4914 martensitic steel",
)

# TODO fit this ourselves
serra_diffusivity_f82h = htm.Diffusivity(
    D_0=1.07e-7,
    E_D=c.J_per_mol_to_eV(13950),
    range=(373, 743),
    source="serra_influence_1997",
    isotope="D",
)
serra_solubility_f82h = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=0.377 * htm.avogadro_nb,
    E_S=c.J_per_mol_to_eV(26880),
    range=(373, 743),
    source="serra_influence_1997",
    isotope="D",
    note="F82H",
)


# TODO fit this ourselves
serra_diffusivity_batman = htm.Diffusivity(
    D_0=1.9e-7,
    E_D=c.J_per_mol_to_eV(15190),
    range=(373, 743),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)
serra_solubility_batman = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=0.198 * htm.avogadro_nb,
    E_S=c.J_per_mol_to_eV(24703),
    range=(373, 743),
    source="serra_influence_1997",
    isotope="D",
    note="Batman steel",
)

# TODO: try and fit this ourselves (Figures 10 and 11)
pisarev_diffusivity = htm.Diffusivity(
    D_0=8.6e-4 * 1e-4,  # cm2 to m2
    E_D=0.075,
    range=(573, 873),
    isotope="D",
    source="pisarev_surface_2001",
    note="F82H",
)

pisarev_solubility = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=2.0e18 * 1e6,  # cm-3 to m-3
    E_S=0.343,
    range=(573, 873),
    isotope="D",
    source="pisarev_surface_2001",
)


# TODO: fit this ourselves from the paper
esteban_diffusivity_h = htm.Diffusivity(
    D_0=5.489e-8,
    E_D=c.J_per_mol_to_eV(10574),
    range=(423, 892),
    isotope="H",
    source="esteban_tritium_2000",
    note="OPTIFER-IVb",
)

esteban_solubility_h = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=0.328 * htm.avogadro_nb,
    E_S=c.J_per_mol_to_eV(29005),
    range=(423, 892),
    isotope="H",
    source="esteban_tritium_2000",
)

esteban_diffusivity_d = htm.Diffusivity(
    D_0=4.613e-8,
    E_D=c.J_per_mol_to_eV(11321),
    range=(423, 892),
    isotope="D",
    source="esteban_tritium_2000",
)

esteban_solubility_d = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=0.325 * htm.avogadro_nb,
    E_S=c.J_per_mol_to_eV(28955),
    range=(423, 892),
    isotope="D",
    source="esteban_tritium_2000",
)


esteban_diffusivity_t = htm.Diffusivity(
    D_0=4.166e-8,
    E_D=c.J_per_mol_to_eV(12027),
    range=(423, 892),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

esteban_solubility_t = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=0.271 * htm.avogadro_nb,
    E_S=c.J_per_mol_to_eV(27905),
    range=(423, 892),
    isotope="T",
    source="esteban_tritium_2000",
    note="extrapolation",
)

# TODO fit the data ourselves (Fig 5 and )
# TODO: Dolinski gives permeability and diffusivities, should we compute solubility ourselves?

dolinski_diffusivity_d = htm.Diffusivity(
    D_0=6.6e-7,
    E_D=c.kJ_per_mol_to_eV(29),
    range=(520, 900),
    isotope="D",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)

dolinski_diffusivity_t = htm.Diffusivity(
    D_0=5.0e-7,
    E_D=c.kJ_per_mol_to_eV(29),
    range=(520, 900),
    isotope="T",
    source="dolinski_heavy_2000",
    note="DIN 1.4914 (MANET) steel",
)


# TODO: fit this ourselves Figures 2, 3
kulsartov_diffusivity_h = htm.Diffusivity(
    D_0=2.8e-8,
    E_D=c.kJ_per_mol_to_eV(8.0),
    range=(400 + 273.15, 600 + 273.15),
    isotope="H",
    source="kulsartov_investigation_2006",
    note="F85H steel",
)

kulsartov_solubility_h = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=7.7 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(33),
    range=(400 + 273.15, 600 + 273.15),
    isotope="H",
    source="kulsartov_investigation_2006",
)


kulsartov_diffusivity_d = htm.Diffusivity(
    D_0=2.3e-8,
    E_D=c.kJ_per_mol_to_eV(7.8),
    range=(400 + 273.15, 600 + 273.15),
    isotope="D",
    source="kulsartov_investigation_2006",
)
kulsartov_solubility_d = htm.Solubility(
    units="m-3 Pa-1/2",
    S_0=7.4 * htm.avogadro_nb,
    E_S=c.kJ_per_mol_to_eV(36),
    range=(400 + 273.15, 600 + 273.15),
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
    prop.material = "rafm_steel"

htm.database += properties
