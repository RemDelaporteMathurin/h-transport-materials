"""Named transformations applied by the build, in the order given in a record.

Value transformations act on every value present (reported pre-exponential
factor or constant, data points, author fit) unless the record restricts
them with ``applies_to``. assume_range acts on the validity range.

Plain unit conversion is never a transformation: it is done implicitly.
Fitting data points is not one either: the build always fits them (see
fit_arrhenius) and the record says which law is used.
"""

import re
from dataclasses import dataclass, field

import numpy as np
import scipy.stats as stats

import h_transport_materials as htm

from .units import parse_quantity_string, ureg


@dataclass
class State:
    """Pint quantities flowing through the build for one record"""

    target_unit: object
    reported: object = None  # pre_exp (arrhenius) or value (constant)
    act_energy: object = None
    range: tuple | None = None
    temperature: object = None
    points_T: object = None
    points_y: object = None
    author_fit_pre_exp: object = None
    author_fit_act_energy: object = None
    context: dict = field(default_factory=dict)  # record, materials, elements
    derived: dict = field(default_factory=dict)  # intermediate values worth reporting
    log: list = field(default_factory=list)

    def value_targets(self, applies_to):
        names = {
            "reported": "reported",
            "points": "points_y",
            "author_fit": "author_fit_pre_exp",
        }
        wanted = applies_to or list(names)
        return [names[w] for w in wanted if getattr(self, names[w]) is not None]

    def map_values(self, fn, applies_to):
        targets = self.value_targets(applies_to)
        if not targets:
            raise ValueError(f"no values to transform among {applies_to}")
        for attr in targets:
            setattr(self, attr, fn(getattr(self, attr)))
        return targets


def gas_volume_to_amount(state, params, applies_to):
    """n = pV / (R T_ref): converts a gas amount given as pressure x volume"""
    T_ref = parse_quantity_string(params["T_ref"])
    return state.map_values(lambda y: y / (htm.Rg * T_ref), applies_to)


def sieverts_constant_to_solubility(state, params, applies_to):
    """S = 1 / Ks, where Ks = p^0.5 / c is the Sieverts constant"""
    concentration_unit = ureg.Unit(params.get("concentration_unit", "dimensionless"))
    return state.map_values(lambda y: 1 / y * concentration_unit, applies_to)


def density(material, T=None):
    """Density of a material from the registry, evaluated at T if it varies"""
    rho = material.density
    if rho is None:
        raise ValueError(f"material {material.id} has no density in the registry")
    if rho.form == "constant":
        return ureg.Quantity(rho.value, ureg.Unit(rho.unit))
    if T is None:
        raise ValueError(f"density of {material.id} depends on temperature: set density_at")
    T = T.to(ureg.Unit(rho.T_unit)).magnitude
    if rho.range is not None and not rho.range.value[0] <= T <= rho.range.value[1]:
        raise ValueError(f"density_at {T} is outside the correlation range {rho.range.value}")
    return ureg.Quantity(rho.a + rho.b * T, ureg.Unit(rho.unit))


def parse_formula(formula):
    """'BeF2' -> {'Be': 1, 'F': 2}"""
    parts = re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", formula)
    if not parts or "".join(el + n for el, n in parts) != formula:
        raise ValueError(f"cannot parse chemical formula {formula!r}")
    counts = {}
    for el, n in parts:
        counts[el] = counts.get(el, 0) + (float(n) if n else 1)
    return counts


def molar_mass(composition, elements):
    """Mean molar mass of a mixture given in mol %.

    ``composition`` maps elements (at.%) or formulas (mol % of formula
    units) to their percentage: {"Li": 17, "Pb": 83} or {"LiF": 66, "BeF2": 34}.
    """
    weights = elements.atomic_weights
    unit = ureg.Unit(elements.unit)
    total = ureg.Quantity(0, unit)
    for formula, percent in composition.items():
        counts = parse_formula(formula)
        missing = set(counts) - set(weights)
        if missing:
            raise ValueError(f"no atomic weight for {sorted(missing)} in the element table")
        M = sum(n * weights[el] for el, n in counts.items())
        total = total + percent / 100 * ureg.Quantity(M, unit)
    return total


def _composition(ctx, params, per):
    """The composition a fraction refers to: per atom or per formula unit"""
    key = "composition" if per == "atom" else "formula_units"
    if "molar_mass_from" in params:
        candidates = [ctx["materials"][params["molar_mass_from"]]]
    else:
        candidates = [ctx["record"].sample, ctx["materials"][ctx["record"].material]]
    for c in candidates:
        if getattr(c, key) is not None:
            return getattr(c, key)
    raise ValueError(f"no {key.replace('_', ' ')} to compute the molar mass per {per} from")


def _density(ctx, params):
    if "density" in params:
        return parse_quantity_string(params["density"])
    material = ctx["materials"][params.get("density_from", ctx["record"].material)]
    T = parse_quantity_string(params["density_at"]) if "density_at" in params else None
    return density(material, T)


def mole_fraction_to_concentration(state, params, applies_to):
    """c = x * rho / M: mole fraction to concentration.

    The density and molar mass come from the material registry unless given
    explicitly (``density``, ``molar_mass``: quantity strings, for values
    cited from the paper). Params:

    - ``per``: ``atom`` (default; x per atom of the material, M is the mean
      atomic mass) or ``formula_unit`` (x per formula unit, e.g. per LiF or
      BeF2 in FLiBe)
    - ``density_from``: material id (default: the record's material)
    - ``density_at``: temperature at which a temperature-dependent density
      is evaluated
    - ``molar_mass_from``: material id (default: the record's sample, else
      its material)
    """
    ctx = state.context
    per = params.get("per", "atom")
    if per not in ("atom", "formula_unit"):
        raise ValueError(f"per must be atom or formula_unit, not {per!r}")
    rho = _density(ctx, params)
    if "molar_mass" in params:
        M = parse_quantity_string(params["molar_mass"])
    else:
        M = molar_mass(_composition(ctx, params, per), ctx["elements"])

    number_density = (rho / M).to(ureg.mol * ureg.m**-3)
    state.derived["density"] = rho
    state.derived["molar_mass"] = M.to(ureg.kg / ureg.mol)
    state.derived["number_density"] = number_density
    return state.map_values(lambda y: y * number_density, applies_to)


def mass_to_volume_basis(state, params, applies_to):
    """c_volume = c_mass * rho: from per unit mass (e.g. per gram) to per unit volume"""
    rho = _density(state.context, params)
    state.derived["density"] = rho
    return state.map_values(lambda y: y * rho, applies_to)


def concentration_ratio_to_solubility(state, params, applies_to):
    """S = K / (R T): Henry solubility from K = c_dissolved / c_gas (dimensionless).

    Evaluated at each data point's temperature, or at the temperature of a
    constant, so it does not apply to an Arrhenius law.
    """
    if state.points_y is not None:
        state.points_y = state.points_y / (htm.Rg * state.points_T)
        return ["points"]
    if state.temperature is not None:
        state.reported = state.reported / (htm.Rg * state.temperature.to(ureg.K))
        return ["reported"]
    raise ValueError("needs data points or a constant at a given temperature")


NOMINAL_MASSES = {"H": 1, "D": 2, "T": 3}


def isotope_scaling(state, params, applies_to):
    """y_isotope = y_from * (m_isotope / m_from) ** exponent

    For diffusivities the classical scaling is exponent -0.5. Nominal masses
    (1, 2, 3) are used.
    """
    from_isotope = params["from_isotope"]
    to_isotope = state.context["record"].isotope
    factor = (NOMINAL_MASSES[to_isotope] / NOMINAL_MASSES[from_isotope]) ** params["exponent"]
    state.derived["isotope_factor"] = ureg.Quantity(factor)
    return state.map_values(lambda y: y * factor, applies_to)


def fit_arrhenius(T, y, unit):
    """Unweighted least squares on ln(y) vs 1/T (same algorithm as ArrheniusProperty.fit)

    Returns:
        dict: pre_exp, act_energy, range and rvalue of the fit
    """
    T = T.to(ureg.K)
    y = y.to(unit)
    keep = ~(np.isnan(T.magnitude) | np.isnan(y.magnitude))
    T, y = T[keep], y[keep]
    res = stats.linregress(1 / T.magnitude, np.log(y.magnitude))
    return {
        "pre_exp": np.exp(res.intercept) * y.units,
        "act_energy": -(res.slope * ureg.K) * htm.k_B,
        "range": (T.min(), T.max()),
        "rvalue": res.rvalue,
    }


def max_relative_difference(law_a, law_b, T_range, n=200):
    """Largest |a / b - 1| between two Arrhenius laws over a temperature range

    Returns:
        tuple: (max relative difference, temperature where it occurs)
    """
    T = np.linspace(T_range[0].m_as(ureg.K), T_range[1].m_as(ureg.K), n) * ureg.K

    def value(law):
        return law["pre_exp"] * np.exp(-law["act_energy"] / (htm.k_B * T))

    ratio = (value(law_a) / value(law_b)).to(ureg.dimensionless).magnitude
    i = np.argmax(np.abs(ratio - 1))
    return float(abs(ratio[i] - 1)), T[i]


def assume_range(state, params, applies_to):
    """Sets a validity range that the paper does not give"""
    low, high = params["range"]
    unit = ureg.Unit(params.get("unit", "K"))
    state.range = (ureg.Quantity(low, unit), ureg.Quantity(high, unit))
    return ["range"]


REGISTRY = {
    "gas_volume_to_amount": gas_volume_to_amount,
    "sieverts_constant_to_solubility": sieverts_constant_to_solubility,
    "mole_fraction_to_concentration": mole_fraction_to_concentration,
    "mass_to_volume_basis": mass_to_volume_basis,
    "concentration_ratio_to_solubility": concentration_ratio_to_solubility,
    "isotope_scaling": isotope_scaling,
    "assume_range": assume_range,
}


def apply(state, transformation):
    fn = REGISTRY[transformation.op]
    touched = fn(state, transformation.params, transformation.applies_to)
    state.log.append({"op": transformation.op, "applied_to": touched})
