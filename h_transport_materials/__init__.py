from importlib import metadata

try:
    __version__ = metadata.version("h-transport-materials")
except Exception:
    __version__ = "unknown"

import pint
from scipy import constants

ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
pint.set_application_registry(ureg)

# CODATA values (exact in the 2019 SI)
k_B = constants.k / constants.e * ureg.eV * ureg.particle**-1 * ureg.K**-1
Rg = constants.R * ureg.Pa * ureg.m**3 * ureg.mol**-1 * ureg.K**-1
avogadro_nb = constants.N_A * ureg.particle * ureg.mol**-1

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
from . import plotting
from .helpers import *
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


def get(record_id: str, path=None):
    """Returns a property from the record database by its id.

    Usage::

        D = htm.get("htm:W-D-H-frauenfelder1969")
        D.record["reported"]  # as published

    Args:
        record_id (str): the permanent record id
        path (str, optional): a compiled database file (e.g. attached to a
            GitHub release). Defaults to the one shipped with the package.

    Returns:
        ArrheniusProperty: the property, with the full record in ``.record``
    """
    from .records.loader import get as _get

    return _get(record_id, path)


def load(path=None):
    """Returns the record database as a PropertiesGroup.

    Args:
        path (str, optional): a compiled database file (e.g. attached to a
            GitHub release). Defaults to the one shipped with the package.
    """
    from .records.loader import properties

    return properties(path)
