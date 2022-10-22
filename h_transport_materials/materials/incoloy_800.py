import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility


schmidt_diffusivity = Diffusivity(
    D_0=9.7e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=56.4 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(1023, 1223),
    isotope="H",
    source="schmidt_studies_1985",
    note="sample No. 1.2 Material 1.4876 (second line of Table 2 in Schmidt's paper)"
    + "in Shimada 2020 review, the S_0 factor is wrong",
)

schmidt_permeability_S_0 = (
    6.34e-8
    * htm.ureg.mol
    * htm.ureg.meter**-1
    * htm.ureg.second**-1
    * htm.ureg.Pa**-0.5
)  # according to Shimada 2020
schmidt_permeability_E_S = 56.6 * htm.ureg.kJ * htm.ureg.mol**-1


schmidt_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=schmidt_permeability_S_0
    / (schmidt_diffusivity.pre_exp * htm.ureg.m**2 * htm.ureg.s**-1),
    E_S=schmidt_permeability_E_S
    - (schmidt_diffusivity.act_energy * htm.ureg.eV * htm.ureg.particle**-1),
    range=(1023, 1223),
    isotope="H",
    source="schmidt_studies_1985",
)

properties = [schmidt_diffusivity, schmidt_solubility]

for prop in properties:
    prop.material = "incoloy_800"

htm.database += properties
