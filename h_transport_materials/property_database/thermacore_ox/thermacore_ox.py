import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("Field_THERMACORE_OX_2018.csv"),
    delimiter=",",
)

OakRidge_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    data_y=data[:,1] * u.mol * u.m**(-1) * u.s**(-1) * u.MPa**(-.5),
    isotope="H",
    source="Field_2018",
)

properties = [
    OakRidge_perm,
]

for prop in properties:
    prop.material = htm.THERMACORE_OX

htm.database += properties