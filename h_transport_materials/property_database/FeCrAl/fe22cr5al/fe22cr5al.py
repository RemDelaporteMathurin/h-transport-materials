import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("Xu_Fe22Cr5Al_2016.csv"),
    delimiter=",",
)

xu_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    data_y=data[:,1] * u.mol * u.m**(-1) * u.s**(-1) * u.Pa**(-.5),
    source="xu_studies_2016",
    isotope="D",
    note="Figure 1, oxidised",
)

properties = [
    xu_perm,
]

for prop in properties:
    prop.material = htm.FE22CR5AL

htm.database += properties
