import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

NIOBIUM_MOLAR_VOLUME = 1.08e-8  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/niobium

volkl_diffusivity = Diffusivity(
    D_0=5.00e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=10.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(273, 773),
    source="volkl_5_1975",
    isotope="H",
)

schober_diffusivity = Diffusivity(
    D_0=4.4e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=12.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="schober_h_1990",
    isotope="H",
)

veleckis_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=1.26e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=-35.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(625, 944),
    source="veleckis_thermodynamic_1969",
    isotope="H",
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=3.6e-6
    / NIOBIUM_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=-33.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="reiter_compilation_1996",
    isotope="H",
)

properties = [
    volkl_diffusivity,
    schober_diffusivity,
    veleckis_solubility,
    reiter_solubility,
]

for prop in properties:
    prop.material = "niobium"

htm.database += properties
