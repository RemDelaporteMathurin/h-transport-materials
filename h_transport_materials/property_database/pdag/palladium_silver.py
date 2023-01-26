import h_transport_materials as htm
from h_transport_materials import(
    Diffusivity, 
    Solubility, 
    Permeability,
    DissociationCoeff, 
    RecombinationCoeff)
from pathlib import Path
import numpy as np

serra_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/diffusivity.csv",
    delimiter=",",
    names=True,
)

serra_diffusivity_h = Diffusivity(
    data_T=1000 / serra_diffusivity_data["hydrogenX"] * htm.ureg.K,
    data_y=serra_diffusivity_data["hydrogenY"] * htm.ureg.m**2 * htm.ureg.s**-1,
    isotope="H",
    source="serra_hydrogen_1998-2",
)

serra_diffusivity_d = Diffusivity(
    data_T=1000 / serra_diffusivity_data["deuteriumX"] * htm.ureg.K,
    data_y=serra_diffusivity_data["deuteriumY"] * htm.ureg.m**2 * htm.ureg.s**-1,
    isotope="D",
    source="serra_hydrogen_1998-2",
)

serra_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/serra_1998/solubility.csv",
    delimiter=",",
    names=True,
)

serra_solubility_h = Solubility(
    units="m-3 Pa-1/2",
    data_T=1000 / serra_solubility_data["hydrogenX"] * htm.ureg.K,
    data_y=serra_solubility_data["hydrogenY"]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_1998-2",
)

serra_solubility_d = Solubility(
    units="m-3 Pa-1/2",
    data_T=1000 / serra_solubility_data["deuteriumX"] * htm.ureg.K,
    data_y=serra_solubility_data["deuteriumY"]
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    isotope="D",
    source="serra_hydrogen_1998-2",
)
serra_dissociation_h = DissociationCoeff(
    pre_exp=1.7e-2
    * htm.ureg.mol
    * htm.ureg.m**-2
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1,
    act_energy=26.294 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(323 * htm.ureg.K, 773* htm.ureg.K),
    source="serra_hydrogen_1998-2",
)
serra_dissociation_d = DissociationCoeff(
    pre_exp=1.3e-2
    * htm.ureg.mol
    * htm.ureg.m**-2
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1,
    act_energy=24.780 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(323 * htm.ureg.K, 773* htm.ureg.K),
    source="serra_hydrogen_1998-2",
)
serra_recombination_coeff_h= RecombinationCoeff(
    pre_exp=0.51 * htm.ureg.mol**-1 * htm.ureg.m**4 * htm.ureg.s**-1,
    act_energy=65.490 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(323 * htm.ureg.K, 773 * htm.ureg.K),
    source="serra_hydrogen_1998-1",
) 
serra_recombination_coeff_d= RecombinationCoeff(
    pre_exp=0.39 * htm.ureg.mol**-1 * htm.ureg.m**4 * htm.ureg.s**-1,
    act_energy=61.842 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(323 * htm.ureg.K, 773 * htm.ureg.K),
    source="serra_hydrogen_1998-1",
) 
vadrucci_permeability_wt84 = Permeability(
    pre_exp=2.95e-8 * u.mol * htm.ureg.m**-1 * htm.ureg.u.s**-1 * htm.ureg.u.Pa**-0.5,
    act_energy=2531.49 * htm.ureg.J * htm.ureg.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_pdag_2013",
    note="wt = 84 micron"
)
vadrucci_permeability_wt150 = Permeability(
    pre_exp=5.63e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=5456.06 * htm.ureg..J * htm.ureg.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_pdag_2013",
    note="wt = 150 micron"
)
vadrucci_permeability_wt200 = Permeability(
    pre_exp=2.06e-8 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=2592.56 * htm.ureg..J * htm.ureg.mol**-1,
    range=(473 * u.K, 623 * u.K),
    isotope="H",
    source="vadrucci_pdag_2013",
    note="wt = 200 micron"
)
vadrucci_dissociation_h = DissociationCoeff(
    pre_exp=2.05e-3
    * htm.ureg.mol
    * htm.ureg.m**-2
    * htm.ureg.s**-1
    * htm.ureg.Pa**-1,
    act_energy=20.103 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(473* htm.ureg.K, 623* htm.ureg.K),
    source="vadrucci_pdag_2013",
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
