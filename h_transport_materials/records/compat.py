"""Converts built records into the existing htm property objects.

This is the compatibility layer: code using ``htm.diffusivities.filter(...)``
keeps working when the database is loaded from compiled records.
"""

import h_transport_materials as htm

from .doi import normalize_doi
from .units import ENERGY_UNIT, ureg

CLASSES = {
    "diffusivity": htm.Diffusivity,
    "solubility": htm.Solubility,
    "permeability": htm.Permeability,
    "recombination_coeff": htm.RecombinationCoeff,
    "dissociation_coeff": htm.DissociationCoeff,
}

LAWS = {"sieverts": "sievert", "henry": "henry", None: None}


def _quantity(d):
    return ureg.Quantity(d["value"], ureg.Unit(d["unit"]))


def _legacy_bib_key(source):
    """Key of the matching references.bib entry (by DOI), so author, year and
    bibdata work as today. Falls back to the source key."""
    if source.get("doi"):
        doi = normalize_doi(source["doi"])
        for key, entry in htm.bib_database.entries.items():
            if normalize_doi(entry.fields.get("doi", "")) == doi:
                return key
    return source["key"]


def to_property(built, materials, sources):
    """Builds an htm property object from a built record

    Args:
        built (dict): one entry of build()["records"]
        materials (dict): material id -> material dict
        sources (dict): source key -> source dict

    Returns:
        htm.ArrheniusProperty: the property, with the record id attached as
            ``prop.record_id`` and the full record as ``prop.record``
    """
    n = built["normalized"]
    if n["selected"] == "constant":
        T = _quantity(n["temperature"])
        pre_exp, act_energy, T_range = _quantity(n["value"]), 0 * ENERGY_UNIT, (T, T)
    else:
        pre_exp, act_energy = _quantity(n["pre_exp"]), _quantity(n["act_energy"])
        T_range = (
            tuple(ureg.Quantity(v, ureg.K) for v in n["range"]["value"])
            if n["range"]
            else None
        )

    source = sources[built["source"]["key"]]
    kwargs = dict(
        pre_exp=pre_exp,
        act_energy=act_energy,
        range=T_range,
        isotope=built["isotope"],
        source=_legacy_bib_key(source),
        note=built["note"],
    )
    cls = CLASSES[built["property"]]
    if built["property"] in ("solubility", "permeability"):
        kwargs["law"] = LAWS[built["law"]]
    if cls is htm.Solubility:
        kwargs["S_0"], kwargs["E_S"] = kwargs.pop("pre_exp"), kwargs.pop("act_energy")
    elif cls is htm.Diffusivity:
        kwargs["D_0"], kwargs["E_D"] = kwargs.pop("pre_exp"), kwargs.pop("act_energy")

    prop = cls(**kwargs)
    if "points" in n:
        # set after construction so the selected fit is kept, not refitted
        prop.data_T = _quantity(n["points"]["T"])
        prop.data_y = _quantity(n["points"]["y"])

    material = materials[built["material"]]
    legacy = material.get("htm_legacy")
    prop.material = getattr(htm, legacy) if legacy else htm.Material(material["name"])
    prop.record_id = built["id"]
    prop.record = built
    return prop


def to_properties_group(db):
    """Builds an htm.PropertiesGroup from a compiled database (dict)"""
    materials = {m["id"]: m for m in db["materials"]}
    sources = {s["key"]: s for s in db["sources"]}
    return htm.PropertiesGroup(
        to_property(r, materials, sources) for r in db["records"]
    )
