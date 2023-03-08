import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
    DissociationCoeff,
    RecombinationCoeff,
)
from pathlib import Path
import numpy as np

u = htm.ureg

serra_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/diffusivity.csv",
    delimiter=",",
    names=True,
)

serra_diffusivity_h = Diffusivity(
    data_T=1000 / serra_diffusivity_data["hydrogenX"] * u.K,
    data_y=serra_diffusivity_data["hydrogenY"] * u.m**2 * u.s**-1,
    isotope="H",
    source="serra_hydrogen_1998-2",
)

serra_diffusivity_d = Diffusivity(
    data_T=1000 / serra_diffusivity_data["deuteriumX"] * u.K,
    data_y=serra_diffusivity_data["deuteriumY"] * u.m**2 * u.s**-1,
    isotope="D",
    source="serra_hydrogen_1998-2",
)

serra_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/solubility.csv",
    delimiter=",",
    names=True,
)

serra_solubility_h = Solubility(
    data_T=1000 / serra_solubility_data["hydrogenX"] * u.K,
    data_y=serra_solubility_data["hydrogenY"] * u.mol * u.m**-3 * u.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_1998-2",
)

serra_solubility_d = Solubility(
    data_T=1000 / serra_solubility_data["deuteriumX"] * u.K,
    data_y=serra_solubility_data["deuteriumY"] * u.mol * u.m**-3 * u.Pa**-0.5,
    isotope="D",
    source="serra_hydrogen_1998-2",
)
serra_dissociation_h = DissociationCoeff(
    pre_exp=1.7e-2 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=26.294 * u.kJ * u.mol**-1,
    isotope="H",
    range=(323 * u.K, 773 * u.K),
    source="serra_hydrogen_1998-2",
)
serra_dissociation_d = DissociationCoeff(
    pre_exp=1.3e-2 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=24.780 * u.kJ * u.mol**-1,
    isotope="D",
    range=(323 * u.K, 773 * u.K),
    source="serra_hydrogen_1998-2",
)
serra_recombination_coeff_h = RecombinationCoeff(
    pre_exp=0.51 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=65.490 * u.kJ * u.mol**-1,
    isotope="H",
    range=(323 * u.K, 773 * u.K),
    source="serra_hydrogen_1998-1",
)
serra_recombination_coeff_d = RecombinationCoeff(
    pre_exp=0.39 * u.mol**-1 * u.m**4 * u.s**-1,
    act_energy=61.842 * u.kJ * u.mol**-1,
    isotope="D",
    range=(323 * u.K, 773 * u.K),
    source="serra_hydrogen_1998-1",
)
vadrucci_permeability_wt84 = Permeability(
    pre_exp=2.95e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=2531.49 * u.J * u.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_hydrogen_2013",
    note="wt = 84 micron",
)
vadrucci_permeability_wt150 = Permeability(
    pre_exp=5.63e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=5456.06 * u.J * u.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_hydrogen_2013",
    note="wt = 150 micron",
)
vadrucci_permeability_wt200 = Permeability(
    pre_exp=2.06e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=2592.56 * u.J * u.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_hydrogen_2013",
    note="wt = 200 micron",
)

# TODO fit this ourselves
R_S_0 = 4.88e2 * u.mol**-1 * u.m**2 * u.s * u.Pa
E_R_S = -20.103 * u.kJ * u.mol**-1
vadrucci_dissociation_h = DissociationCoeff(
    pre_exp=2 / R_S_0,
    act_energy=-E_R_S,
    isotope="H",
    range=(473 * u.K, 623 * u.K),
    source="vadrucci_hydrogen_2013",
    note="equation 17 + probably an error in the units of the activation energy in the original paper",
)

properties = [
    serra_diffusivity_h,
    serra_diffusivity_d,
    serra_solubility_h,
    serra_solubility_d,
    serra_dissociation_h,
    serra_dissociation_d,
    serra_recombination_coeff_h,
    serra_recombination_coeff_d,
    vadrucci_permeability_wt84,
    vadrucci_permeability_wt150,
    vadrucci_permeability_wt200,
    vadrucci_dissociation_h,
]

for prop in properties:
    prop.material = htm.PDAG

htm.database += properties
