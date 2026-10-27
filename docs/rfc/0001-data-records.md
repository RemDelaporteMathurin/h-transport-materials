# RFC 0001: HTM data as records

Status: draft for discussion
Prototype: `h_transport_materials/records/`, `data/`, `tests/test_records.py`

## 1. Why

HTM exists to stop errors propagating between published experiments and the
people who use them. Today the database works against that goal in four ways:

- **Records are code.** Each property is a Python constructor call, so the
  data can only be read, checked or contributed by people who read Python.
- **The published values are lost.** pint normalises everything at import
  time; `database.json` only holds SI values. Nobody can check an entry
  against the paper without redoing the conversion.
- **Conversions are inline arithmetic.** About 160 of the ~464 entries pass
  computed values (gas volumes, densities, composition factors). That is
  where recent bugs were found (Schumacher 50x, Houben ms vs s, Frauenfelder
  reference temperature) and where the prototype found more (section 9).
- **The authors' own fits are discarded.** Entries with data points are
  refitted by HTM and the refit replaces the published law.

## 2. Principles

1. Store what the paper prints: values, units and the form of the law.
2. Everything HTM does to the data is a named transformation with
   parameters and a rationale, and says whether it comes from the paper or
   is HTM's own choice.
3. Every record points to a citable source and, ideally, to the location of
   the value in it (table, equation, figure).
4. Normalised values are derived, never typed by hand.

## 3. Records

One YAML file per **source x property x isotope x material**, in
`data/records/`. The file name is the record id.

**Id**: `htm:<MAT>-<PROP>-<ISO>-<author><year>[-a]`, for example
`htm:W-S-H-frauenfelder1969`. `<MAT>` is the material code from the
registry, `<PROP>` is one of `D S P Kr Kd`. A letter suffix separates two
records that would otherwise collide (two samples in one paper). Ids are
permanent: a wrong record is deprecated, never deleted, so citations of an
id keep resolving.

A complete example, the Frauenfelder 1969 tungsten solubility:

```yaml
id: htm:W-S-H-frauenfelder1969
property: solubility
law: sieverts
material: tungsten
isotope: H
method: unknown
source:
  key: frauenfelder1969
  location: null
reported:
  form: arrhenius
  pre_exp:
    value: 2.9e-1
    unit: "torr * L / cm^3 / torr^0.5"
  act_energy: {value: 24000, unit: "cal/mol"}
  range: {value: [1100, 2400], unit: K}
transformations:
  - op: gas_volume_to_amount
    params: {T_ref: "273 K"}
    origin: paper
    rationale: the paper gives the dissolved amount as a gas volume (torr L) at 273 K
curation:
  status: draft
  flags:
    - fill method and location from the paper
```

The blocks:

| Block | Content |
|---|---|
| identity | `id`, `property`, `law` (solubility and permeability only), `material`, `isotope` |
| `method` | controlled vocabulary: `gas-absorption`, `gas-permeation`, `time-lag`, `isovolumetric-desorption`, `tds`, `ion-implantation`, `electrochemical`, `isotope-extrapolation`, `dft`, `md`, `review`, `unknown` |
| `sample` | composition (at.%), form, purity, surface; all optional |
| `source` | `key` into `data/sources/`, `location` in the paper, `via` if the value was taken from a review |
| `reported` | the values as printed (below) |
| `transformations` | ordered list (section 4) |
| `note` | free text, kept short; anything structured gets a field |
| `curation` | `status` (draft, verified, disputed), contributors, verifiers, open `flags`, `errata` |

### `reported` forms

- `arrhenius`: `pre_exp`, `act_energy`, optional `range` and uncertainties.
- `constant`: a single `value` at a single `temperature` (Fauvet 1988).
  No fake temperature range.
- `points`: a CSV next to the record, with an axis description for each
  column (`quantity`, `unit`, `scale: linear | ln | log10`, `factor` for
  axes like 1000/T) so the file holds what was digitised, not a
  pre-converted copy. Optional `digitised_from` (figure), `wpd_project`, and
  `author_fit`.
- `author_fit` takes the form printed: `arrhenius` (pre-factor and energy)
  or `ln_linear` (ln y = intercept + slope / T, as Schumacher prints it).

Units are strings that pint parses with HTM's registry (which adds
`ccSTP`, `ccNTP`, `atfr`). When the typeset unit differs from what HTM
believes the paper means, `unit_as_printed` keeps the original and a
curation flag says why (Fauvet, section 9).

A range is only filled in if the paper gives one. Otherwise it stays
`null` and an `assume_range` transformation, marked `origin: htm`, supplies
one.

## 4. Transformations

Each transformation is `{op, params, origin, rationale, applies_to}`:

- `origin: paper` means the paper itself states the step (a reference
  temperature, a definition). `origin: htm` means it is HTM's choice. HTM's
  choices are listed for every record in the build output
  (`htm_assumptions`) so a user sees them next to the value.
- `applies_to` restricts a value transformation to `reported`, `points` or
  `author_fit` (default: all present).
- Plain unit conversion is never listed; the build does it.

Initial vocabulary, each a small tested function in
`records/transforms.py`:

| op | does | params |
|---|---|---|
| `gas_volume_to_amount` | n = pV / (R T_ref) | `T_ref` |
| `sieverts_constant_to_solubility` | S = 1 / Ks | `concentration_unit` |
| `atom_fraction_to_concentration` | c = x rho / M | `density`, `molar_mass` |
| `refit_arrhenius` | unweighted fit of ln y against 1/T | none |
| `assume_range` | validity range not given in the paper | `range`, `unit` |

To come with the migration: `extrapolate_composition` (Chan 1984),
`isotope_scaling`, `average` (only in the evaluations layer, section 8).

Density and molar mass are parameters, not hidden constants, so every
record that relies on the Pb-17Li density says so.

## 5. Registries

`data/materials/<id>.yaml`: id, code (used in record ids), name,
`families` as a list (fixes `Compound` being a subclass of `Metal`),
symbol, composition, aliases, and `htm_legacy` (the `htm` material object
used by the compatibility layer). Li50Pb50 and Pb-17Li are separate
materials grouped by the `lithium-lead` family.

`data/sources/<key>.yaml`: CSL-like fields (type, title, authors, year,
journal, volume, issue, pages), DOI, URL, open access URL, and
`bibtex_key` linking to the current `references.bib`. During migration the
bib file stays the reference for author and year; afterwards it is
generated from the source files.

## 6. Build and artefacts

`python -m h_transport_materials.records.build`:

1. validates every material, source and record (pydantic models in
   `records/models.py`; ids, file names, references between files);
2. parses units and reads point files;
3. applies transformations in order;
4. selects the Arrhenius parameters: the reported law, or for points the
   HTM refit if `refit_arrhenius` is listed, else the author fit;
5. converts to the normalised SI units used today and checks dimensions.

The output is one JSON file with every record as stored plus a
`normalized` block, `htm_assumptions` and a transformation log. The YAML
is never written to. Release artefacts: `htm-data-<calver>.json`, later
Parquet and CSV, attached to the GitHub release and shipped in the wheel.
`python -m h_transport_materials.records.schema` exports JSON Schemas so
records can be validated without Python (editors, other languages).

**Versioning.** Data releases use calendar versions (`2026.11`), the
library keeps semantic versions. Each library release declares the data
version it bundles; `htm.load(version="2026.11")` loads another one.

## 7. Library API

The current API keeps working: `htm.database`, `htm.diffusivities`,
`.filter(...)`, `.value(T)`, pint quantities. `records/compat.py` already
turns built records into today's property objects, with the record
attached (`prop.record_id`, `prop.record`).

New:

```python
D = htm.get("htm:W-D-H-frauenfelder1969")
D.reported          # as printed
D.transformations   # what HTM did
D.htm_assumptions   # HTM's own choices only
db = htm.load(version="2026.11")
```

The `property_database/` modules are removed once every record is
migrated, after one release where both exist and the equivalence test
passes on all of them.

## 8. Curation and contributions

- A record starts as `draft`. It becomes `verified` when a second person
  has checked it against the PDF and cleared its flags. `disputed` marks a
  record with an unresolved conflict (Fauvet).
- Recommended or averaged values are a separate evaluations layer with its
  own authors. They never overwrite records.
- Contribution tiers: an issue form that a GitHub Action turns into a
  draft YAML pull request; YAML pull requests with `htm new` and
  `htm validate`; library code.
- CI on pull requests: schema and dimension checks, plausibility bounds,
  DOI resolution, duplicate detection, and a bot comment plotting the new
  record against existing ones for the same material.

## 9. What the prototype showed

Five sources were chosen because each stresses a different part of the
model. They give 12 records:

| Source | Records | Stresses |
|---|---|---|
| Frauenfelder 1969, W | D, S (H) | gas volume units, reference temperature |
| Esteban 2001, W | D, S for H, D, T | one source, six records; T extrapolated |
| Heinola 2010, W | D (H) | DFT, no range in the paper |
| Fauvet 1988, Pb-17Li | D, S (H) | single temperature |
| Schumacher 1990, Li50Pb50 | S (H) | digitised points, author fit, composition |

**Equivalence.** Built and converted back to property objects, all 12
records reproduce the current database: pre-exponential factors are
identical and activation energies agree to 1e-17 eV. The one intended
difference is Fauvet's range, now the 450 degC (723.15 K) of the paper
instead of a fake 722 to 724 K (issue #37). `tests/test_records.py`
enforces this and lists the difference explicitly.

**Findings the current format was hiding:**

1. **Schumacher's own fit was dropped.** The abstract gives
   ln(x_H sqrt(1e5 Pa) / sqrt(p)) = -A + B/T with A = 8.17, B = 734 K.
   HTM's refit of the digitised points gives an activation energy of
   -0.0565 eV against -0.0632 eV from the authors' fit, and a pre-factor
   10% higher; the digitised points are noisy (r = 0.89).
2. **Schumacher is converted with the wrong density.** The atom fraction
   is converted with the Li50Pb50 molar mass but the Pb-17Li density.
3. **Fauvet's diffusivity unit is uncertain.** The abstract prints
   1.5e-9 mm2/s; HTM stores 1.5e-9 m2/s, which is the plausible value. The
   record keeps both and is marked `disputed` until someone checks the body
   of the paper. The abstract also gives an uncertainty of 0.2e-8 on the
   Sieverts constant, now stored.
4. **Esteban's tritium values are extrapolated**, not measured (abstract).
   They now carry `method: isotope-extrapolation`.
5. **Heinola's range is HTM's.** The 300 to 1200 K range is not in the
   paper; it is now an `assume_range` transformation with `origin: htm`.

## 10. Migration

1. Auto-convert the ~300 entries built from literal values by capturing
   constructor arguments before pint converts them.
2. Hand-transcribe the ~160 computed ones, starting with the CSV-backed
   ones. Density and composition entries get a transformation each; expect
   more findings like section 9.
3. Gate: the equivalence test over all records, with every intended
   difference listed and explained.
4. Verification sprint on W, 316L, Pb-17Li, EUROFER97 and FLiBe.

## 11. Open points

1. Schumacher: select the authors' fit instead of HTM's refit? This would
   be the first deliberate value change; same question for every record
   with points and a published fit.
2. Schumacher: find a Li50Pb50 density, or keep the Pb-17Li one as a
   labelled assumption.
3. Fauvet: confirm the diffusivity unit from the body of the paper.
4. Constants: HTM uses `R = 8.314` and `k_B = 8.617e-5`. Moving to CODATA
   values changes every converted number slightly; do it as one labelled
   data release.
5. Where `data/` lives in the wheel: ship only the compiled JSON, or the
   YAML too?
6. Should `constant` records appear in `htm.diffusivities` at all, given
   they have no activation energy? They currently appear as an Arrhenius
   law with zero activation energy over a zero-width range.
