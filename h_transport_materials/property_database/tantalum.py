import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


volkl_diffusivity = Diffusivity(
    D_0=4.40e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=13.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(253 * htm.ureg.K, 573 * htm.ureg.K),
    isotope="H",
    source="volkl_5_1975",
)

veleckis_solubility = Solubility(
    S_0=1.32e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=-33.7 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(623 * htm.ureg.K, 904 * htm.ureg.K),
    source="veleckis_thermodynamic_1969",
)

properties = [volkl_diffusivity, veleckis_solubility]

for prop in properties:
    prop.material = htm.TANTALUM

htm.database += properties
