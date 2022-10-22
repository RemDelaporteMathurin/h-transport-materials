import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


causey_diffusivity = Diffusivity(
    D_0=0.93e-4 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=2.8 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(900, 1473),
    source="causey_interaction_1989",
    isotope="H",
)

atsumi_diffusivity = Diffusivity(
    D_0=1.69 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=251 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500 + 273.15, 900 + 273.15),
    isotope="D",
    source="atsumi_absorption_1988",
    note="Equation 5 of Atsumi's paper",
)

atsumi_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.9e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=-19.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="atsumi_absorption_1988",
    isotope="H",
)

properties = [causey_diffusivity, atsumi_diffusivity, atsumi_solubility]

for prop in properties:
    prop.material = "carbon"

htm.database += properties
