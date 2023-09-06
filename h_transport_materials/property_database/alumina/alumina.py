import h_transport_materials as htm
from h_transport_materials import (
    Diffusivity,
    Solubility,
    Permeability,
)
import numpy as np

u = htm.ureg

serra_data = np.genfromtxt(
    htm.absolute_path("serra_2005/data.csv"),
    delimiter=",",
    names=True,
)

serra_permeability = Permeability(
    data_T=1 / serra_data["permx"] * u.K,
    data_y=serra_data["permy"] * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_diffusivity = Diffusivity(
    data_T=1 / serra_data["diffx"] * u.K,
    data_y=serra_data["diffy"] * u.m**2 * u.s**-1,
    isotope="H",
    source="serra_hydrogen_2004",
)

serra_solubility = Solubility(
    data_T=1 / serra_data["solx"] * u.K,
    data_y=serra_data["soly"] * u.mol * u.m**-3 * u.Pa**-0.5,
    isotope="H",
    source="serra_hydrogen_2004",
)


belonshko_data = np.genfromtxt(
    htm.absolute_path("belonoshko_2004/data.csv"),
    delimiter=",",
    names=True,
)

belonshko_diffusivity_solid = Diffusivity(
    data_T=1 / belonshko_data["alpha_aluminax"] * u.K,
    data_y=belonshko_data["alpha_aluminay"] * u.m**2 * u.s**-1,
    isotope="H",
    source="belonoshko_first-principles_2004",
    note="solid alpha alumina",
)

belonshko_diffusivity_liquid = Diffusivity(
    data_T=1 / belonshko_data["liquid_aluminax"] * u.K,
    data_y=belonshko_data["liquid_aluminay"] * u.m**2 * u.s**-1,
    isotope="H",
    source="belonoshko_first-principles_2004",
    note="liquid alumina",
)


fowler_data = np.genfromtxt(
    htm.absolute_path("fowler_1977/data.csv"),
    delimiter=",",
    names=True,
)

fowler_diffusivity_single_crystal = Diffusivity(
    data_T=1 / fowler_data["single_crystalX"] * u.K,
    data_y=fowler_data["single_crystalY"] * u.cm**2 * u.s**-1,
    isotope="T",
    source="fowler_tritium_1977",
    note="single crystal",
)

fowler_diffusivity_powder = Diffusivity(
    data_T=1 / fowler_data["powderX"] * u.K,
    data_y=fowler_data["powderY"] * u.cm**2 * u.s**-1,
    isotope="T",
    source="fowler_tritium_1977",
    note="powder",
)

fowler_diffusivity_sintered = Diffusivity(
    data_T=1 / fowler_data["sinteredX"] * u.K,
    data_y=fowler_data["sinteredY"] * u.cm**2 * u.s**-1,
    isotope="T",
    source="fowler_tritium_1977",
    note="powder",
)

fowler_diffusivity_doped = Diffusivity(
    data_T=1 / fowler_data["mgOdopedX"] * u.K,
    data_y=fowler_data["mgOdopedY"] * u.cm**2 * u.s**-1,
    isotope="T",
    source="fowler_tritium_1977",
    note="MgO doped",
)

properties = [
    serra_permeability,
    serra_diffusivity,
    serra_solubility,
    belonshko_diffusivity_solid,
    belonshko_diffusivity_liquid,
    fowler_diffusivity_single_crystal,
    fowler_diffusivity_powder,
    fowler_diffusivity_sintered,
    fowler_diffusivity_doped,
]

for prop in properties:
    prop.material = htm.ALUMINA

htm.database += properties
