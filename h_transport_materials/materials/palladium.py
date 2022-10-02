import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c

import numpy as np

PALLADIUM_MOLAR_VOLUME = 8.85e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/palladium

volkl_diffusivity = ArrheniusProperty(
    pre_exp=2.90e-7,
    act_energy=c.kJ_per_mol_to_eV(22.2),
    range=(223, 873),
    source="volkl_5_1975",
    isotope="H",
)


# TODO: try and fit the data ourself https://www.osti.gov/biblio/4413386


favreau_data_T = np.array(
    [
        200.75,
        306.0,
        400.0,
        200.5,
        305.0,
        399.5,
        398.25,
        400.0,
        402.0,
        395.65,
        399.5,
        401.5,
        298.5,
        296.38,
        305.5,
        298.0,
        300.0,
        199.5,
        201.2,
        205.33,
        200.25,
        303.0,
        401.25,
    ]
)  # in degC Table II

favreau_data_T += 273.15  # in K

favreau_data_y = np.array(
    [
        0.17225,
        0.17470,
        0.1066,
        0.12335,
        0.1267,
        0.1227,
        0.1343,
        0.12515,
        0.1089,
        0.1083,
        0.1173,
        0.1004,
        0.1045,
        0.11095,
        0.1038,
        0.1073,
        0.1298,
        0.1205,
        0.1255,
        0.1292,
        0.1285,
        0.1219,
        0.1039,
    ]
)  # in cc STP per gram of palladium  cmHg^-1.2

favreau_data_y = favreau_data_y  # TODO to mol T per gram of Pd  cmHg-1.2
favreau_data_y = favreau_data_y  # TODO to mol T m-3  cmHg-1.2
favreau_data_y = favreau_data_y  # TODO to mol T m-3  Pa-1.2
favreau_data_y = favreau_data_y  # TODO to T m-3  Pa-1.2


favreau_solubility_t = Solubility(
    units="m-3 Pa-1/2",
    data_T=favreau_data_T,
    data_y=favreau_data_y,
    # pre_exp=4.45e-1 * htm.avogadro_nb,
    # act_energy=c.kJ_per_mol_to_eV(-8.4),
    source="favreau_solubility_1954",
    isotope="T",
)

palladium_diffusivities = [volkl_diffusivity]

palladium_solubilities = [favreau_solubility_t]

for prop in palladium_diffusivities + palladium_solubilities:
    prop.material = "palladium"

diffusivities.properties += palladium_diffusivities
solubilities.properties += palladium_solubilities
