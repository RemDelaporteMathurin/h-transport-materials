import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

kishimoto_diffusivity = Diffusivity(
    D_0=4.90e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.44 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873, 1173),
    source="kishimoto_hydrogen_1985",
)

kishimoto_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.62e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=0.22 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="H",
    range=(873, 1173),
    source="kishimoto_hydrogen_1985",
    note="the units for the S_0onential factor in Kishimoto's paper is weird so took the conversion from Shimada 2020",
)

properties = [kishimoto_diffusivity, kishimoto_solubility]

for prop in properties:
    prop.material = "inconel_600"

htm.database += properties
