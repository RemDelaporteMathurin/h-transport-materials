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

bib_database = parse_file(str(Path(__file__).parent) + '/references.bib')

from .property import Property, ArrheniusProperty, Solubility
from .properties_group import PropertiesGroup

diffusivities = PropertiesGroup()
solubilities = PropertiesGroup()
from .materials import *

from . import fitting
from . import plotting
