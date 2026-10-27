"""Pydantic models for HTM data records, materials and sources.

A record stores a property exactly as published (``reported``) plus the
ordered list of ``transformations`` HTM applies to it. Normalised SI values
are never stored in the YAML: they are computed by the build.
"""

import re
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = "0.1.0"

PropertyName = Literal[
    "diffusivity",
    "solubility",
    "permeability",
    "recombination_coeff",
    "dissociation_coeff",
]

PROPERTY_CODES = {
    "diffusivity": "D",
    "solubility": "S",
    "permeability": "P",
    "recombination_coeff": "Kr",
    "dissociation_coeff": "Kd",
}

Isotope = Literal["H", "D", "T"]

Method = Literal[
    "gas-absorption",
    "gas-permeation",
    "time-lag",
    "isovolumetric-desorption",
    "tds",
    "ion-implantation",
    "electrochemical",
    "isotope-extrapolation",
    "dft",
    "md",
    "review",
    "unknown",
]

TransformationOp = Literal[
    "gas_volume_to_amount",
    "sieverts_constant_to_solubility",
    "atom_fraction_to_concentration",
    "refit_arrhenius",
    "assume_range",
]

ID_PATTERN = re.compile(
    r"^htm:(?P<material>[A-Za-z0-9]+)-(?P<property>D|S|P|Kr|Kd)-(?P<isotope>H|D|T)"
    r"-(?P<source>[a-z]+[0-9]{4}[a-z]?)(?P<suffix>-[a-z])?$"
)
SOURCE_KEY_PATTERN = r"^[a-z]+[0-9]{4}[a-z]?$"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Quantity(_Strict):
    """A value with a unit string parseable by pint (with HTM's extra units)."""

    value: float
    unit: str
    unit_as_printed: str | None = Field(
        None, description="Unit exactly as typeset in the paper, when it differs"
    )


class Uncertainty(_Strict):
    value: float
    unit: str
    kind: Literal["absolute", "relative", "std", "range"] = "absolute"


class Range(_Strict):
    value: tuple[float, float]
    unit: str = "K"

    @field_validator("value")
    @classmethod
    def increasing(cls, v):
        if not v[0] < v[1]:
            raise ValueError(f"range must be strictly increasing, got {v}")
        return v


class ArrheniusFit(_Strict):
    """value = pre_exp * exp(-act_energy / (k_B T))"""

    form: Literal["arrhenius"]
    pre_exp: Quantity
    act_energy: Quantity
    range: Range | None = None
    location: str | None = None


class LnLinearFit(_Strict):
    """ln(value / y_unit) = intercept + slope / T, as some papers print it"""

    form: Literal["ln_linear"]
    intercept: float
    slope: Quantity = Field(description="in K")
    y_unit: str
    range: Range | None = None
    location: str | None = None


AuthorFit = Annotated[Union[ArrheniusFit, LnLinearFit], Field(discriminator="form")]


class Axis(_Strict):
    """Describes one column of a digitised CSV as plotted in the paper."""

    column: int
    quantity: Literal["temperature", "inverse_temperature", "value"]
    unit: str
    scale: Literal["linear", "ln", "log10"] = "linear"
    factor: float = Field(1.0, description="e.g. 1000 for a 1000/T axis")


class ArrheniusReported(_Strict):
    form: Literal["arrhenius"]
    pre_exp: Quantity
    act_energy: Quantity
    range: Range | None = Field(
        None, description="Only if given in the paper. Use assume_range otherwise"
    )
    pre_exp_uncertainty: Uncertainty | None = None
    act_energy_uncertainty: Uncertainty | None = None


class ConstantReported(_Strict):
    """A single value at a single temperature."""

    form: Literal["constant"]
    value: Quantity
    temperature: Quantity
    uncertainty: Uncertainty | None = None


class PointsReported(_Strict):
    """Data points (usually digitised) plus the authors' own fit if they gave one."""

    form: Literal["points"]
    file: str = Field(description="CSV next to the record, no header")
    x: Axis
    y: Axis
    digitised_from: str | None = Field(None, description="e.g. 'Fig. 5'")
    wpd_project: str | None = None
    author_fit: AuthorFit | None = None


Reported = Annotated[
    Union[ArrheniusReported, ConstantReported, PointsReported],
    Field(discriminator="form"),
]


class Transformation(_Strict):
    op: TransformationOp
    params: dict[str, Union[str, float, int, list, dict]] = {}
    origin: Literal["paper", "htm"] = Field(
        description="'paper' if the paper states it, 'htm' if it is HTM's own choice"
    )
    rationale: str
    applies_to: list[Literal["reported", "points", "author_fit"]] | None = Field(
        None, description="which values a value transformation acts on (default: all)"
    )


class SourceRef(_Strict):
    """Cites a source by DOI (preferred) or, for sources without a DOI, by key"""

    doi: str | None = None
    key: str | None = Field(None, pattern=SOURCE_KEY_PATTERN)
    location: str | None = Field(None, description="e.g. 'Table 2', 'Eq. 5'")
    via: str | None = Field(None, description="DOI or key of a review, if not read in the original")

    @model_validator(mode="after")
    def doi_or_key(self):
        if (self.doi is None) == (self.key is None):
            raise ValueError("source needs exactly one of doi or key")
        return self


class Sample(_Strict):
    composition: dict[str, float] | None = Field(None, description="atomic %")
    form: str | None = None
    purity: str | None = None
    surface: str | None = None


class Curation(_Strict):
    status: Literal["draft", "verified", "disputed"] = "draft"
    contributed_by: list[str] = []
    verified_by: list[str] = []
    flags: list[str] = Field(
        [], description="open questions a verifier must resolve against the PDF"
    )
    errata: list[str] = []


class Record(_Strict):
    id: str
    property: PropertyName
    law: Literal["sieverts", "henry"] | None = None
    material: str
    isotope: Isotope
    method: Method
    sample: Sample = Sample()
    source: SourceRef
    reported: Reported
    transformations: list[Transformation] = []
    note: str | None = None
    curation: Curation = Curation()

    @field_validator("id")
    @classmethod
    def id_format(cls, v):
        if not ID_PATTERN.match(v):
            raise ValueError(
                f"id {v!r} must look like htm:<MAT>-<D|S|P|Kr|Kd>-<H|D|T>-<author><year>[-a]"
            )
        return v

    @model_validator(mode="after")
    def consistent(self):
        m = ID_PATTERN.match(self.id)
        if m["property"] != PROPERTY_CODES[self.property]:
            raise ValueError(f"id {self.id} does not match property {self.property}")
        if m["isotope"] != self.isotope:
            raise ValueError(f"id {self.id} does not match isotope {self.isotope}")
        if self.source.key is not None and m["source"] != self.source.key:
            raise ValueError(f"id {self.id} does not match source {self.source.key}")
        if self.property in ("solubility", "permeability") and self.law is None:
            raise ValueError(f"{self.property} records need a law (sieverts or henry)")
        ops = [t.op for t in self.transformations]
        if "assume_range" in ops and getattr(self.reported, "range", None) is not None:
            raise ValueError("assume_range is not allowed when the paper gives a range")
        if "refit_arrhenius" in ops and self.reported.form != "points":
            raise ValueError("refit_arrhenius needs reported.form == 'points'")
        return self


class Material(_Strict):
    id: str
    code: str = Field(description="short code used in record ids, e.g. W")
    name: str
    families: list[str] = []
    symbol: str | None = None
    composition: dict[str, float] | None = Field(None, description="atomic %")
    aliases: list[str] = []
    htm_legacy: str | None = Field(
        None, description="name of the htm material object used by the current API"
    )
    note: str | None = None


class Person(_Strict):
    family: str
    given: str | None = None
    orcid: str | None = None


class Source(_Strict):
    """Generated from a DOI or a BibTeX entry by records.sources, then reviewed"""

    key: str = Field(pattern=SOURCE_KEY_PATTERN)
    type: Literal["article", "report", "thesis", "book", "chapter", "conference", "other"]
    title: str
    authors: list[Person]
    year: int
    journal: str | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    doi: str | None = None
    url: str | None = None
    open_access_url: str | None = None
