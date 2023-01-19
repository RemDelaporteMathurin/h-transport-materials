try:
    # Python 3.8+
    from importlib import metadata
except ImportError:
    try:
        import importlib_metadata as metadata
    except ImportError:
        __version__ = "unknown"

try:
    __version__ = metadata.version("h-transport-materials")
except Exception:
    __version__ = "unknown"

import pint

ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
pint.set_application_registry(ureg)

k_B = 8.617e-5 * ureg.eV * ureg.particle**-1 * ureg.K**-1
Rg = 8.314 * ureg.Pa * ureg.m**3 * ureg.mol**-1 * ureg.K**-1
avogadro_nb = 6.022e23 * ureg.particle * ureg.mol**-1

from pybtex.database import parse_file
from pathlib import Path

bib_database = parse_file(str(Path(__file__).parent) + "/references.bib")

from .property import (
    Property,
    ArrheniusProperty,
    Solubility,
    Diffusivity,
    Permeability,
    RecombinationCoeff,
    DissociationCoeff,
)
from .properties_group import PropertiesGroup
from . import conversion
from . import fitting
from . import plotting
from .material import *

database = PropertiesGroup()

from . import property_database

diffusivities = PropertiesGroup(
    prop for prop in database if isinstance(prop, Diffusivity)
)

solubilities = PropertiesGroup(
    prop for prop in database if isinstance(prop, Solubility)
)

permeabilities = PropertiesGroup(
    prop for prop in database if isinstance(prop, Permeability)
)

recombination_coeffs = PropertiesGroup(
    prop for prop in database if isinstance(prop, RecombinationCoeff)
)

dissociation_coeffs = PropertiesGroup(
    prop for prop in database if isinstance(prop, DissociationCoeff)
)
