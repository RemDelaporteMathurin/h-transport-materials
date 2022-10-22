import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability
import h_transport_materials.conversion as c
from h_transport_materials.materials.iron import IRON_MOLAR_VOLUME


reiter_diffusivity = Diffusivity(
    D_0=3.70e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=51.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 10 papers on diffusivity from Reiter compilation review",
)

reiter_solubility = Solubility(
    units="m-3 Pa-1/2",
    S_0=5.8e-6
    / IRON_MOLAR_VOLUME
    * htm.ureg.mol
    * htm.ureg.m**-3
    * htm.ureg.Pa**-0.5,
    E_S=13.1 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(500, 1200),
    isotope="H",
    source="reiter_compilation_1996",
    note="this is an average of 5 papers on diffusivity from Reiter compilation review",
)

houben_permeability = Permeability(
    pre_exp=8e-7
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.mbar**-0.5,
    act_energy=58 * htm.ureg.kJ * htm.ureg.mol**-1,
    source="houben_comparison_2022",
    isotope="D",
)


properties = [reiter_diffusivity, reiter_solubility, houben_permeability]

for prop in properties:
    prop.material = "steel_316l"

htm.database += properties
