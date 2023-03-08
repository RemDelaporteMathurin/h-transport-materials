import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility


hashizume_diffusivity = Diffusivity(
    D_0=7.50e-4 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.13 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(373 * htm.ureg.K, 573 * htm.ureg.K),
    isotope="T",
    source="hashizume_diffusional_2007",
    note="there is a conversion mistake for D_0 in Shimada 2020 review",
)

klepikov_solubility = Solubility(
    data_T=[673.0, 773.0, 873.0, 973.0, 1073.0] * htm.ureg.K,
    data_y=[1.62e20, 9.84e19, 5.65e19, 4.91e19, 2.94e19]
    * htm.ureg.particle
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    isotope="H",
    source="klepikov_hydrogen_2000",
    note="taken from Table 2",
)

properties = [hashizume_diffusivity, klepikov_solubility]

for prop in properties:
    prop.material = htm.V4CR4TI

htm.database += properties
