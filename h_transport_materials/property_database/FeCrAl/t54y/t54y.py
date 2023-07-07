import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("Hu_T54Y_2015.csv"),
    delimiter=",",
)

Hu_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    data_y=data[:,1] * u.mol * u.m**(-1) * u.s**(-1) * u.MPa**(-.5),
    source="hu_hydrogen_2015",
    isotope="H",
    note="Figure 6",
)

properties = [
    Hu_perm,
]

for prop in properties:
    prop.material = htm.T54Y

htm.database += properties
