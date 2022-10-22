import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

IRON_MOLAR_VOLUME = 7.09e-6  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/iron

volkl_diffusivity = Diffusivity(
    D_0=4.00e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=4.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(573, 1073),
    source="volkl_5_1975",
)

tahara_diffusivity_H = Diffusivity(
    D_0=4.43e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=5.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="H",
    range=(500, 1000),
    source="tahara_measurements_1985",
)

tahara_diffusivity_D = Diffusivity(
    D_0=4.28e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=6.47 * htm.ureg.kJ * htm.ureg.mol**-1,
    isotope="D",
    range=(500, 1000),
    source="tahara_measurements_1985",
)

eichenauer_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=4.90e-6
    / IRON_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=24.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(473, 1183),
    isotope="H",
    source="eichenauer_diffusion_1958",
)


properties = [
    volkl_diffusivity,
    tahara_diffusivity_H,
    tahara_diffusivity_D,
    eichenauer_solubility,
]

for prop in properties:
    prop.material = "iron"

htm.database += properties
