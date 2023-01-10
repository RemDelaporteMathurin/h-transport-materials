import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import h_transport_materials.conversion as c

NI_MOLAR_VOLUME = 6.59e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/nickel

volkl_diffusivity = Diffusivity(
    D_0=6.87e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=40.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 1473 * htm.ureg.K),
    isotope="H",
    source="volkl_5_1975",
)

robertson_diffusivity = Diffusivity(
    D_0=3.72e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=40.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(273 * htm.ureg.K, 1673 * htm.ureg.K),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    isotope="H",
    year=1973,
)

louthan_diffusivity_H = Diffusivity(
    D_0=7.0e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=39.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 500 * htm.ureg.K),
    isotope="H",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_D = Diffusivity(
    D_0=7.0e-7 / 2**0.5 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=39.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 500 * htm.ureg.K),
    isotope="D",
    source="louthan_hydrogen_1975",
)

louthan_diffusivity_T = Diffusivity(
    D_0=7.0e-7 / 3**0.5 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=39.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 500 * htm.ureg.K),
    isotope="T",
    source="louthan_hydrogen_1975",
)

robertson_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.52e-6
    / NI_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=12.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(273 * htm.ureg.K, 1673 * htm.ureg.K),
    source="W.M.Robertson: Zeitschrift für Metallkunde, 1973, 64[6], 436-43",
    author="Robertson",
    year=1973,
    isotope="H",
)


louthan_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.5e-1 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=15.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(300 * htm.ureg.K, 500 * htm.ureg.K),
    isotope="H",
    source="louthan_hydrogen_1975",
)


properties = [
    volkl_diffusivity,
    robertson_diffusivity,
    louthan_diffusivity_H,
    louthan_diffusivity_D,
    louthan_diffusivity_T,
    robertson_solubility,
    louthan_solubility,
]

for prop in properties:
    prop.material = "nickel"

htm.database += properties
