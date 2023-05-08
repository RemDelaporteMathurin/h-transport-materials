import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility

u = htm.ureg

TITANIUM_MOLAR_VOLUME = 1.05e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/titanium

reiter_diffusivity = Diffusivity(
    D_0=6.9e-7 * u.m**2 * u.s**-1,
    E_D=49.1 * u.kJ * u.mol**-1,
    source="reiter_compilation_1996",
    isotope="T",
    range=(873 * u.K, 1123 * u.K),
)

reiter_solubility = Solubility(
    S_0=1.06e-5 / TITANIUM_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-42.7 * u.kJ * u.mol**-1,
    range=(873 * u.K, 1123 * u.K),
    isotope="T",
    source="reiter_compilation_1996",
)

properties = [reiter_diffusivity, reiter_solubility]

for prop in properties:
    prop.material = htm.TITANIUM

htm.database += properties
