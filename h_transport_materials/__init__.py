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


k_B = 8.617e-5  # eV/K
Rg = 8.314
avogadro_nb = 6.022e23

from pybtex.database import parse_file
from pathlib import Path

bib_database = parse_file(str(Path(__file__).parent) + "/references.bib")

import pint

ureg = pint.UnitRegistry()

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

database = PropertiesGroup()

from .materials import *

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
