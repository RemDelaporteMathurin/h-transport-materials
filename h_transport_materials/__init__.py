k_B = 8.617e-5  # eV/K
Rg = 8.314
avogadro_nb = 6.022e23
from .property import Property, ArheniusProperty
from .properties_group import PropertiesGroup

diffusivities = PropertiesGroup()
solubilities = PropertiesGroup()
from .materials import *

from . import fitting
from . import plotting
