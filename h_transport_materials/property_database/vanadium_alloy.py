import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

hashizume_diffusivity = Diffusivity(
    D_0=7.50e-4 * u.cm**2 * u.s**-1,
    E_D=0.13 * u.eV * u.particle**-1,
    range=(373 * u.K, 573 * u.K),
    isotope="T",
    source="hashizume_diffusional_2007",
    note="there is a conversion mistake for D_0 in Shimada 2020 review",
)

klepikov_solubility = Solubility(
    data_T=[673.0, 773.0, 873.0, 973.0, 1073.0] * u.K,
    data_y=[1.62e20, 9.84e19, 5.65e19, 4.91e19, 2.94e19]
    * u.particle
    * u.m**-3
    * u.Pa**-0.5,
    isotope="H",
    source="klepikov_hydrogen_2000",
    note="taken from Table 2",
)

properties = [hashizume_diffusivity, klepikov_solubility]

for prop in properties:
    prop.material = htm.V4CR4TI

htm.database += properties
