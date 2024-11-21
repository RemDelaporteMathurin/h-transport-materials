import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)

u = htm.ureg

# diffusivity
data_diffusivity_serra = htm.structure_data_from_wpd("serra_diffusivity_1998.csv")

note_serra_diffusivity_h = (
    "Serra equation doesn't match the experimental points on their graph"
    + "\n Serra gives D_0=5.7e-7 m2/s and E_D = 41220 J/mol \n"
    + "ITER also gives a diffusivity but they adapted it from the wrong equations..."
)
serra_diffusivity_h = Diffusivity(
    data_T=1000 / data_diffusivity_serra["elbrodur_h2"]["x"] * u.K,
    data_y=data_diffusivity_serra["elbrodur_h2"]["y"] * u.m**2 * u.s**-1,
    source="serra_hydrogen_1998",
    isotope="H",
    note=note_serra_diffusivity_h,
)

note_serra_diffusivity_d = (
    "Serra equation doesn't match the experimental points on their graph"
    + "\n Serra gives D_0=4.8e-7 m2/s and E_D = 40370 J/mol \n"
    + "ITER also gives a diffusivity but they adapted it from the wrong equations..."
)
serra_diffusivity_d = Diffusivity(
    data_T=1000 / data_diffusivity_serra["elbrodur_d2"]["x"] * u.K,
    data_y=data_diffusivity_serra["elbrodur_d2"]["y"] * u.m**2 * u.s**-1,
    source="serra_hydrogen_1998",
    isotope="D",
    note=note_serra_diffusivity_d,
)

# solubility
data_solubility_serra = htm.structure_data_from_wpd("serra_solubility_1998.csv")

serra_solubility_h = Solubility(
    data_T=1000 / data_solubility_serra["elbrodur_h"]["x"] * u.K,
    data_y=data_solubility_serra["elbrodur_h"]["y"] * u.mol * u.m**-3 * u.Pa**-0.5,
    source="serra_hydrogen_1998",
    isotope="H",
)

serra_solubility_d = Solubility(
    data_T=1000 / data_solubility_serra["elbrodur_d"]["x"] * u.K,
    data_y=data_solubility_serra["elbrodur_d"]["y"] * u.mol * u.m**-3 * u.Pa**-0.5,
    source="serra_hydrogen_1998",
    isotope="D",
)
# ################# Noh 2016 #############################
nog_diffusivity_cucrzr_t = Diffusivity(
    5.05e-4 * u.m**2 * u.s**-1,
    0.964 * u.eV * u.particle**-1,
    range=(573 * u.K, 873 * u.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

nog_solubility_cucrzr_t_1 = Solubility(
    S_0=7.83e20 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.0715 * u.eV * u.particle**-1,
    range=(573 * u.K, 873 * u.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

nog_solubility_cucrzr_t_2 = Solubility(
    S_0=5.42e23 * u.particle * u.m**-3 * u.Pa**-0.5,
    E_S=0.4 * u.eV * u.particle**-1,
    range=(573 * u.K, 873 * u.K),
    source="noh_hydrogen-isotope_2016",
    isotope="T",
)

# ################# Anderl 1999 #############################
anderl_diffusivity_cucrzr_d = Diffusivity(
    D_0=2.0e-2 * u.m**2 * u.s**-1,
    E_D=1.2 * u.eV * u.particle**-1,
    range=(700 * u.K, 800 * u.K),
    source="anderl_deuterium_1999",
    isotope="D",
)

# ################# Penalva 1999 #############################
penalva_diffusivity_cucrzr_h = Diffusivity(
    3.55e-5 * u.m**2 * u.s**-1,
    65.5e3 * u.J * u.mol**-1,
    range=(593 * u.K, 773 * u.K),
    source="penalva_interaction_2012",
    isotope="D",
)

penalva_solubility_cucrzr_h = Solubility(
    S_0=6.71e-3 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=8.4e3 * u.J * u.mol**-1,
    range=(593 * u.K, 773 * u.K),
    source="penalva_interaction_2012",
    isotope="D",
)

anderl_recombination = RecombinationCoeff(
    pre_exp=2.9e-14 * u.meter**4 * u.second**-1 * u.particle**-1,
    act_energy=1.92 * u.eV * u.particle**-1,
    range=(700.0 * u.K, 800.0 * u.K),
    isotope="D",
    source="anderl_deuterium_1999",
)


houben_permeability = Permeability(
    pre_exp=6e-6 * u.mol * u.m**-1 * u.s**-1 * u.mbar**-0.5,
    act_energy=79 * u.kJ * u.mol**-1,
    range=(u.Quantity(300, u.degC), u.Quantity(550, u.degC)),
    source="houben_comparison_2022",
    isotope="D",
)

properties = [
    serra_diffusivity_h,
    serra_diffusivity_d,
    nog_diffusivity_cucrzr_t,
    anderl_diffusivity_cucrzr_d,
    penalva_diffusivity_cucrzr_h,
    serra_solubility_h,
    serra_solubility_d,
    nog_solubility_cucrzr_t_1,
    nog_solubility_cucrzr_t_2,
    penalva_solubility_cucrzr_h,
    anderl_recombination,
    houben_permeability,
]

for prop in properties:
    prop.material = htm.CUCRZR

htm.database += properties
