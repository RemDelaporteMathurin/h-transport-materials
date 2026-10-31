"""Unit parsing for records.

Records store units as strings. They are parsed with htm's registry, which
includes HTM's extra units (ccSTP, ccNTP, atfr) from conversion.py.
"""

import h_transport_materials as htm
from h_transport_materials import conversion  # noqa: F401  registers ccSTP, ccNTP, atfr

ureg = htm.ureg

ENERGY_UNIT = ureg.eV * ureg.particle**-1

# normalised units, identical to the ones used by the property classes
NORMALIZED_UNITS = {
    ("diffusivity", None): ureg.m**2 * ureg.s**-1,
    ("solubility", "sieverts"): ureg.particle * ureg.m**-3 * ureg.Pa**-0.5,
    ("solubility", "henry"): ureg.particle * ureg.m**-3 * ureg.Pa**-1,
    ("permeability", "sieverts"): ureg.particle
    * ureg.m**-1
    * ureg.s**-1
    * ureg.Pa**-0.5,
    ("permeability", "henry"): ureg.particle * ureg.m**-1 * ureg.s**-1 * ureg.Pa**-1,
    ("recombination_coeff", None): ureg.particle
    * ureg.m**4
    * ureg.s**-1
    * ureg.particle**-2,
    ("dissociation_coeff", None): ureg.particle
    * ureg.m**-2
    * ureg.s**-1
    * ureg.Pa**-1,
}


def unit(s: str):
    """Parses a unit string, raising ValueError with the string on failure"""
    try:
        return ureg.Unit(s)
    except Exception as e:
        raise ValueError(f"cannot parse unit {s!r}: {e}") from e


def quantity(value, unit_str: str):
    """Builds a pint Quantity from a magnitude and a unit string"""
    return ureg.Quantity(value, unit(unit_str))


def parse_quantity_string(s: str):
    """Parses '273 K' or '10163.197 kg/m^3' into a pint Quantity"""
    try:
        return ureg.Quantity(s)
    except Exception as e:
        raise ValueError(f"cannot parse quantity {s!r}: {e}") from e
