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


def atom_fraction_to_concentration(state, params, applies_to):
    """c = x * rho / M: atom fraction to concentration using a density and molar mass"""
    density = parse_quantity_string(params["density"])
    molar_mass = parse_quantity_string(params["molar_mass"])
    atom_density = density / molar_mass
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
