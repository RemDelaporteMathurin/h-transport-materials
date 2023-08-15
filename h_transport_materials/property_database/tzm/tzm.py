import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
) 
import numpy as np

u = htm.ureg

data = np.genfromtxt(
    htm.absolute_path("forcey_TZM_1993.csv"),
    delimiter=",",
)

forcey_perm = Permeability(
    data_T=(1000 / data[:,0]) * u.K,
    data_y=data[:,1] * u.mol * u.m**(-1) * u.s**(-1) * u.Pa**(-0.5),
    source="forcey_permeability_1993",
    isotope="D",
    note="Figure 3",
)

properties = [
    forcey_perm,
]

for prop in properties:
    prop.material = htm.TZM

htm.database += properties
