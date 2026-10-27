"""Named transformations applied by the build, in the order given in a record.

Value transformations act on every value present (reported pre-exponential
factor or constant, data points, author fit) unless the record restricts
them with ``applies_to``. Structural transformations (refit_arrhenius,
assume_range) act on the selected Arrhenius parameters.

Plain unit conversion is never a transformation: it is done implicitly.
"""

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
    refit: dict | None = None
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


def molar_mass(composition, elements):
    """Molar mass of a composition given in at.%"""
    weights = elements.atomic_weights
    missing = set(composition) - set(weights)
    if missing:
        raise ValueError(f"no atomic weight for {sorted(missing)} in the element table")
    unit = ureg.Unit(elements.unit)
    return sum(
        (at / 100 * ureg.Quantity(weights[el], unit) for el, at in composition.items()),
        start=ureg.Quantity(0, unit),
    )


def atom_fraction_to_concentration(state, params, applies_to):
    """c = x * rho / M: atom fraction to concentration.

    The density and molar mass come from the material registry unless given
    explicitly (``density``, ``molar_mass``: quantity strings, for values
    cited from the paper). Params:

    - ``density_from``: material id (default: the record's material)
    - ``density_at``: temperature at which a temperature-dependent density
      is evaluated
    - ``molar_mass_from``: material id (default: the record's sample
      composition, else its material)
    """
    ctx = state.context
    if "density" in params:
        rho = parse_quantity_string(params["density"])
    else:
        material = ctx["materials"][params.get("density_from", ctx["record"].material)]
        T = parse_quantity_string(params["density_at"]) if "density_at" in params else None
        rho = density(material, T)

    if "molar_mass" in params:
        M = parse_quantity_string(params["molar_mass"])
    else:
        if "molar_mass_from" in params:
            composition = ctx["materials"][params["molar_mass_from"]].composition
        else:
            composition = (
                ctx["record"].sample.composition
                or ctx["materials"][ctx["record"].material].composition
            )
        if composition is None:
            raise ValueError("no composition to compute the molar mass from")
        M = molar_mass(composition, ctx["elements"])

    atom_density = (rho / M).to(ureg.mol * ureg.m**-3)
    state.derived["density"] = rho
    state.derived["molar_mass"] = M.to(ureg.kg / ureg.mol)
    state.derived["atom_density"] = atom_density
    return state.map_values(lambda y: y * atom_density, applies_to)


def refit_arrhenius(state, params, applies_to):
    """Unweighted least squares on ln(y) vs 1/T (same algorithm as ArrheniusProperty.fit)"""
    T = state.points_T.to(ureg.K)
    y = state.points_y.to(state.target_unit)
    keep = ~(np.isnan(T.magnitude) | np.isnan(y.magnitude))
    T, y = T[keep], y[keep]
    res = stats.linregress(1 / T.magnitude, np.log(y.magnitude))
    state.refit = {
        "pre_exp": np.exp(res.intercept) * y.units,
        "act_energy": -(res.slope * ureg.K) * htm.k_B,
        "range": (T.min(), T.max()),
        "rvalue": res.rvalue,
    }
    return ["refit"]


def assume_range(state, params, applies_to):
    """Sets a validity range that the paper does not give"""
    low, high = params["range"]
    unit = ureg.Unit(params.get("unit", "K"))
    state.range = (ureg.Quantity(low, unit), ureg.Quantity(high, unit))
    return ["range"]


REGISTRY = {
    "gas_volume_to_amount": gas_volume_to_amount,
    "sieverts_constant_to_solubility": sieverts_constant_to_solubility,
    "atom_fraction_to_concentration": atom_fraction_to_concentration,
    "refit_arrhenius": refit_arrhenius,
    "assume_range": assume_range,
}


def apply(state, transformation):
    fn = REGISTRY[transformation.op]
    touched = fn(state, transformation.params, transformation.applies_to)
    state.log.append({"op": transformation.op, "applied_to": touched})
