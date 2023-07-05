import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("Ashdown_OX_1605_1980.csv"),
    delimiter=",",
)

ash_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    #this data is given in micro mol: convert to mol
    data_y=data[:,1] *1e-6 * u.mol * u.m**(-1) * u.s**(-1) * u.kPa**(-.5),
    source="ASHDOWN_1980",
    isotope="H",
)

properties = [
    ash_perm,
]

for prop in properties:
    prop.material = htm.OXIDIZED_1605

htm.database += properties