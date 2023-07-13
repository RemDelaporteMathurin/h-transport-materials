import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("Vandeventer_THERMACORE_1980.csv"),
    delimiter=",",
)

van_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    data_y=data[:,1] * u.micromol * u.m**(-1) * u.s**(-1) * u.kPa**(-.5),
    source="vandeventer_hydrogen_1980",
    isotope="H",
    note="Figure 2",
)

properties = [
    van_perm,
]

for prop in properties:
    prop.material = htm.THERMACORE

htm.database += properties
