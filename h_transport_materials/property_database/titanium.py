import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c


TITANIUM_MOLAR_VOLUME = 1.05e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/titanium

reiter_diffusivity = Diffusivity(
    D_0=6.9e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=49.1 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="reiter_compilation_1996",
    isotope="T",
    range=(873 * htm.ureg.K, 1123 * htm.ureg.K),
)

reiter_solubility = Solubility(
    S_0=1.06e-5
    / TITANIUM_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=-42.7 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(873 * htm.ureg.K, 1123 * htm.ureg.K),
    isotope="T",
    source="reiter_compilation_1996",
)

properties = [reiter_diffusivity, reiter_solubility]

for prop in properties:
    prop.material = htm.TITANIUM

htm.database += properties
