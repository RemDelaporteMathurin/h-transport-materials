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
  doi: 10.1116/1.1492699
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
| `source` | the `doi` (or, without a DOI, the `key` of a source file), `location` in the paper, `via` if the value was taken from a review |
| `reported` | the values as printed (below) |
| `transformations` | ordered list (section 4) |
| `note` | free text, kept short; anything structured gets a field |
| `curation` | `status` (draft, verified, disputed), contributors, verifiers, open `flags`, `errata` |

### `reported` forms

- `arrhenius`: `pre_exp`, `act_energy`, optional `range` and uncertainties.
- `log_linear`: the law as many papers print it,
  log_base(y / y_unit) = intercept + slope / T, with `base` e or 10 and
  either a `slope` (in K) or an `act_energy` as printed (for
  ln S = -14.5 + 18.2 kJ/mol / RT). Molybdenum (Katsuta), lithium
  (Veleckis) and graphite (Shirasu) are printed this way; the current code
  hides it as `np.exp(-14.5)`.
- `constant`: a single `value` at a single `temperature` (Fauvet 1988).
  No fake temperature range.
- `points`: a CSV next to the record, with an axis description for each
  column (`quantity`, `unit`, `scale: linear | ln | log10`, `factor` for
  axes like 1000/T) so the file holds what was digitised, not a
  pre-converted copy. Optional `digitised_from` (figure), `wpd_project`, and
  `author_fit`.
- `author_fit` takes the form printed: `arrhenius` or `log_linear`
  (Schumacher prints ln y = -A + B/T).
- `derived`: a law computed from other records, such as S = P / D or
  Kr = Kd / S^2. The record lists its inputs with a power each
  (`[{record: P, power: 1}, {record: D, power: -1}]`); the build multiplies
  the pre-exponential factors and adds the activation energies with those
  powers, after building the inputs (a derived record can use another).
  The range is the overlap of the inputs', an explicit `range`, or the
  range of one input (`range_from`). The record says who derived it
  (`origin`) and why, and an HTM derivation is listed with HTM's
  assumptions. The current database has 14 of these, all computed in HTM.

### Author fit or data points

Published fits are sometimes wrong, and so are published points; nothing
in the paper tells which. So HTM never picks silently:

1. The build always fits the points itself (unweighted, ln y against
   1/T) and keeps both laws in the output, with the largest relative
   difference between them over the measured range. Laws are compared as
   curves, not by their parameters: the pre-factor and the activation
   energy trade off against each other, so the parameters can differ a
   lot while the curves agree (Schumacher: pre-factor x0.91, energy
   -0.007 eV, curves within 2.4%).
2. If the two agree within the tolerance (10%), the authors' fit is used.
3. If they don't, the build fails until a curator records a choice:

   ```yaml
   selected: htm_refit       # or author_fit
   selection_note: >-
     author fit inconsistent with Fig. 3 points (-35% at 600 K);
     cannot tell which is wrong; HTM refits the points
   ```

   The note is mandatory, and a selected HTM refit is listed with HTM's
   assumptions next to the value.
4. Without an author fit, the HTM refit is used and listed as an HTM
   assumption.

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
- Plain unit conversion is never listed; the build does it. Neither is
  fitting points: the build always does it, and the record only says which
  law is used (section 3).

The vocabulary, each a small tested function in `records/transforms.py`.
It comes from the computed patterns actually found in the current
database, not from a wish list:

| op | does | params | used by |
|---|---|---|---|
| `gas_volume_to_amount` | n = pV / (R T_ref) | `T_ref` | Frauenfelder (W, Mo) |
| `sieverts_constant_to_solubility` | S = 1 / Ks | `concentration_unit` | Schumacher |
| `mole_fraction_to_concentration` | c = x rho / M | `per` (`atom` or `formula_unit`), `density_from`, `density_at`, `molar_mass_from`, or explicit `density`, `molar_mass` | Pb-17Li, Li, graphite, SiC, FLiBe (Field) |
| `mass_to_volume_basis` | c = c_mass rho | `density_from`, `density_at` | palladium (Favreau, per gram) |
| `concentration_ratio_to_solubility` | S = K / (R T), at each point's T | none | FLiBe (Malinauskas, Kc) |
| `isotope_scaling` | y (m_iso / m_from) ^ exponent, nominal masses | `from_isotope`, `exponent` | nickel (Louthan, D and T from H) |
| `assume_range` | validity range not given in the paper | `range`, `unit` | Heinola |

An `extrapolate_composition` op is not needed: where a value is
extrapolated to another composition (Chan 1984), the paper did it, so it
is the record's method and note, not an HTM step. Averages belong to the
evaluations layer (section 8).

Material properties are not typed into records. A transformation names
where they come from and the build looks them up:

```yaml
- op: mole_fraction_to_concentration
  params:
    per: atom               # or formula_unit (x per LiF or BeF2 in FLiBe)
    density_from: lipb      # default: the record's material
    density_at: "300 K"     # needed when the density depends on T
  origin: htm
```

The molar mass is computed from the sample composition (or the
material's), per atom or per formula unit, with the element table; the
build reports the density, molar mass and number density it used for each
record. So every record that relies on the
Pb-17Li density says so, a density borrowed from another material is
visible, and a correction to a material fixes every record that uses it.

## 5. Registries

`data/materials/<id>.yaml`: id, code (used in record ids), name,
`families` as a list (fixes `Compound` being a subclass of `Metal`),
symbol, `composition` (at.% of elements) and, for compounds and salts,
`formula_units` (mol % of formulas: `{LiF: 66, BeF2: 34}`), both summing
to 100, aliases, `density` and `htm_legacy` (the `htm` material object used
by the compatibility layer). Li50Pb50 and Pb-17Li are separate materials
grouped by the `lithium-lead` family. The prototype registers tungsten,
Pb-17Li, Li50Pb50, graphite, FLiBe, palladium, SiC, lithium, nickel and
molybdenum.

A `density` is `constant` or `linear` in temperature (rho = a + b T, with
an optional validity range the build enforces) and cites its source like a
record does. Several current constants come from web pages (aqua-calc,
PubChem) or have no source at all; those carry a `url` or a `flags` entry,
and the build refuses a density with neither a source, a URL nor a flag:

```yaml
density:
  form: linear
  a: 10520.35
  b: -1.19051
  unit: kg/m^3
  source: {doi: 10.1016/j.jnucmat.2008.02.016}
```

`data/elements.yaml` holds the atomic weights (with their source) used to
compute molar masses. Other material properties needed by future
transformations (lattice constants, molar volumes) go in the material file
the same way.

`data/sources/<key>.yaml`: CSL-like fields (type, title, authors, year,
journal, volume, issue, pages), DOI, URL, open access URL.

**Nobody writes source files by hand.** A record cites its source by DOI
alone, and the source file is generated from it:

```
htm source add 10.1116/1.1492699     # one DOI (a doi.org URL also works)
htm source sync                      # every DOI cited by a record but missing
htm source from-bib refs.bib         # grey literature without a DOI
```

- Metadata comes from doi.org (CSL-JSON content negotiation), which covers
  Crossref and DataCite DOIs. It is cleaned (markup in titles, Unicode
  hyphens, initials such as `G.A` become `G. A.`, article numbers used as
  pages) and the key is derived from the first author and year
  (`frauenfelder1969`, then `frauenfelder1969b` on a collision).
- The open access URL comes from Unpaywall, which requires a contact
  email: `--email` or `HTM_UNPAYWALL_EMAIL`. It is skipped otherwise.
- The generated file is **committed**, not fetched at build time: builds
  stay offline and reproducible, and when Crossref metadata is wrong the
  file is corrected and the fix is reviewed like any other change.
- Sources without a DOI (KIT and OSTI reports, theses) are imported from a
  BibTeX entry pasted from Zotero or Google Scholar; the record then cites
  the `key`.
- BibTeX is an export, not the store: one shared `.bib` file is a merge
  conflict in every pull request, and BibTeX escaping leaks into titles.
  The build will generate a `references.bib` for people citing HTM data in
  LaTeX.

Prototype check: deleting the five hand-written source files and running
`htm source sync` regenerated them identical, field for field. During
migration the compatibility layer finds the current `references.bib`
entry by DOI, so author, year and `bibdata` behave as today.

## 6. Build and artefacts

`python -m h_transport_materials.records.build`:

1. validates every material, source and record (pydantic models in
   `records/models.py`; ids, file names, references between files);
2. parses units and reads point files;
3. applies transformations in order;
4. selects the Arrhenius parameters: the reported law, or for points the
   author fit or the HTM refit (section 3);
5. converts to the normalised SI units used today and checks dimensions.

The output is one JSON file with every record as stored plus a
`normalized` block, `htm_assumptions`, the material values used
(`derived`: density, molar mass) and a transformation log. The YAML is
never written to. `htm schema` exports JSON Schemas so records can be
validated without Python (editors, other languages).

**What ships where.**

| Artefact | Contains |
|---|---|
| wheel (`pip install`) | the compiled JSON only |
| sdist and GitHub release | `data/` (YAML, CSV) plus the compiled JSON, later Parquet and CSV tables |
| Zenodo | each GitHub release, with a DOI |

How the JSON gets into the wheel: the release workflow runs
`htm build --out h_transport_materials/_data/htm-data.json` before
`python -m build`, and `_data/*.json` is package data. The file is never
committed (`.gitignore`). From a git checkout or an editable install,
`htm.get` and `htm.load` build it from `data/` on first use (with the
`build` extra), cache it next to the package, and rebuild it when a file
in `data/` changes. A CI job builds a wheel, installs it in a clean
environment and reads a record with pydantic and pyyaml absent.

The compiled JSON already holds every record in full (as printed,
transformations, curation, points), so the YAML would add nothing to the
wheel. Leaving it out avoids a second copy that could disagree, about
9 MB of digitiser projects, and a runtime dependency on pydantic and
pyyaml (the library reads one JSON file at import). Anyone who wants to
rebuild with different choices, say densities at the measurement
temperature, gets `data/` from the repository or a release.

**Constants.** HTM defined its own rounded `k_B = 8.617e-5 eV/K` and
`R = 8.314 J/mol/K`, while pint converts kJ/mol to eV with exact values, so
a law gave slightly different values depending on how its activation
energy was entered. `htm.k_B`, `htm.Rg` and `htm.avogadro_nb` now come from
`scipy.constants` (CODATA; branch `fix/codata-constants`). Values move by
at most 0.15% over each validity range (median 0.016%). The records build
uses the same `htm` constants, so the equivalence test is unaffected.

**Versioning.** Data releases use calendar versions (`2026.11`), the
library keeps semantic versions. Each library release declares the data
version it bundles; `htm.load(version="2026.11")` loads another one.

## 7. Library API

The current API keeps working: `htm.database`, `htm.diffusivities`,
`.filter(...)`, `.value(T)`, pint quantities. `records/compat.py` already
turns built records into today's property objects, with the record
attached (`prop.record_id`, `prop.record`).

New (implemented, reading the compiled JSON):

```python
D = htm.get("htm:W-D-H-frauenfelder1969")   # a Diffusivity, as today
D.record["reported"]          # as printed
D.record["transformations"]   # what HTM did
D.record["htm_assumptions"]   # HTM's own choices only
records = htm.load()                         # PropertiesGroup of all records
older = htm.load("htm-data-v0.19.0.json")    # a release's compiled file
```

`htm.load(version=...)` downloading a release's file is left for later;
for now a downloaded file is passed by path. Reading needs no extra
dependencies (no pydantic, no pyyaml).

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
  duplicate detection, and a bot comment plotting the new record against
  existing ones for the same material. If a record cites a DOI with no
  source file, the bot runs `htm source sync` and commits the result, so a
  contributor only ever types the DOI.

## 9. What the prototype showed

Five sources were first chosen because each stresses a different part of
the model; six more were added to exercise every form and transformation
the migration needs. 19 records:

| Source | Records | Stresses |
|---|---|---|
| Frauenfelder 1969, W | D, S (H) | gas volume units, reference temperature |
| Esteban 2001, W | D, S for H, D, T | one source, six records; T extrapolated |
| Heinola 2010, W | D (H) | DFT, no range in the paper |
| Fauvet 1988, Pb-17Li | D, S (H) | single temperature |
| Schumacher 1990, Li50Pb50 | S (H) | digitised points, author fit, composition |
| Louthan 1975, Ni | D (D, T) | isotope scaling |
| Favreau 1954, Pd | S (T) | per gram data, temperatures in degC |
| Malinauskas 1974, FLiBe | S (H) | Henry constant as a concentration ratio |
| Shirasu 1993, graphite | S (H), IG-110U | log form with an energy, one grade of several |
| Katsuta 1982, Mo | D (H) | log form with a slope |
| Veleckis 1974, Li | S (H) | log form, atom fraction in a liquid metal |

**Equivalence.** Built and converted back to property objects, the 19
records reproduce the current database (pre-exponential factors to 1e-12,
activation energies to 1e-15 eV) except for intended differences, each
listed in `tests/test_records.py`:

- Fauvet's range is now the 450 degC (723.15 K) of the paper instead of a
  fake 722 to 724 K (issue #37).
- Schumacher uses the authors' fit instead of HTM's refit of the
  digitised points; the two agree within 2.4% over the measured range.
- Lithium (+0.014%) and palladium (-0.0003%): the registry stores the
  densities the cited pages give, where the code stored a molar volume
  and a specific volume derived from them.
- Candido 2022 (two Pb-17Li solubilities, -1.5%): single values at
  573 K instead of a fake 572 to 574 K range, converted with the molar
  mass of the Pb-15.7Li sample of the thesis instead of Pb-17Li.

**Findings the current format was hiding:**

1. **Schumacher's own fit was dropped.** The abstract gives
   ln(x_H sqrt(1e5 Pa) / sqrt(p)) = -A + B/T with A = 8.17, B = 734 K.
   HTM refitted the digitised points instead. The parameters look
   different (activation energy -0.0565 eV against -0.0632 eV, pre-factor
   10% higher) but the two laws agree within 2.4% over the measured range,
   so the authors' fit is now used.
2. **Schumacher is converted with the wrong density.** The atom fraction
   is converted with the Li50Pb50 molar mass but the Pb-17Li density.
   More generally, HTM's Pb-17Li density constant (10163.197 kg/m3) is the
   Mas de les Valls (2008) correlation 10520.35 - 1.19051 T evaluated at
   300 K, below the melting point (about 508 K), for liquid metal
   measured at 573 to 1100 K. At 723 K the density is about 5% lower.
3. **Fauvet's diffusivity unit is uncertain.** The abstract prints
   1.5e-9 mm2/s; HTM stores 1.5e-9 m2/s, which is the plausible value. The
   record keeps both and is marked `disputed` until someone checks the body
   of the paper. The abstract also gives an uncertainty of 0.2e-8 on the
   Sieverts constant, now stored.
4. **Esteban's tritium values are extrapolated**, not measured (abstract).
   They now carry `method: isotope-extrapolation`.
5. **Heinola's range is HTM's.** The 300 to 1200 K range is not in the
   paper; it is now an `assume_range` transformation with `origin: htm`.
6. **The Li molar mass in `lipb.py` is 10 times too large**
   (0.06941 kg/mol instead of 0.006941 kg/mol). Every Pb-17Li solubility
   converted from an atom fraction is about 6% too low, and the Li50Pb50
   one 29% too low. It surfaced as soon as molar masses were computed from
   a cited table instead of typed by hand. Fixed on `main` in #318 (after
   0.18.3); the existing test had missed it because it checked HTM's value
   with the same faulty helper.
7. **Room temperature densities are used for liquids and hot solids.**
   Besides Pb-17Li (finding 2), lithium solubilities (Veleckis, 983 to
   1176 K) use the density of solid lithium at room temperature
   (534 kg/m3), about 10% above the liquid's. FLiBe solubilities from
   Field 1967 use a mole-fraction average of the densities of solid LiF
   and BeF2 (2.42 g/cm3), about 20% above liquid FLiBe at 500 to 700 degC
   (about 2.0 g/cm3, Romatoski and Hu 2017).
8. **Graphite uses the crystal density.** The Shirasu solubilities are
   converted with 2.266 g/cm3, the theoretical density of graphite; the
   IG-110U and other grades are about 1.7 to 1.9 g/cm3. Whether the bulk
   density applies depends on how the paper defines its H/C ratio, which
   a verifier needs to check.
9. **Frauenfelder's reference temperature differs between papers.** The W
   solubility uses 273 K and the Mo permeability 300 K for the gas volume
   conversion. Both may be right; each needs checking against its paper.
10. **Derived properties mix isotopes and ranges.** The 304 permeability
    attributed to Braun 1980 (deuterium) is Braun's deuterium diffusivity
    times a protium solubility (Hawkins 1953, a report HTM never found,
    cited through Braun), over the diffusivity's range although the
    solubility covers another. The dissociation coefficient computed from
    the same solubility uses the diffusivity's range too. Both records are
    flagged.
11. **The 316L "molar volume" is a number density.**
    `STEEL_316L_MOLAR_VOLUME` is density / molar mass (mol/m3), so
    multiplying by it is right, but the molar mass (56.52 g/mol) is typed by
    hand with a TODO to compute it from the composition. It is now an
    explicit parameter of the transformation, and the 316L density
    (8.0 g/cm3) is in the registry with its handbook source.
12. **Field 1967 measured hydrogen fluoride, not hydrogen.** The two FLiBe
    "H" and "D" solubilities from Field 1967 are the solubilities of HF and
    DF ("The solubilities of hydrogen fluoride and deuterium fluoride in
    molten fluorides"). The records keep the current isotopes and are
    flagged; they probably should not be in `htm.solubilities` for H2/D2.
13. **Molar volumes from a web page.** The copper, gold, nickel, titanium,
    yttrium and zirconium solubilities divide an atom fraction by a molar
    volume from aqua-calc (room temperature solids, iron has no source at
    all). They are now explicit `molar_volume` parameters with their URL.
14. **Some `references.bib` entries are wrong or incomplete.** The Begun
    yttrium paper is filed as 2008 but its DOI is a 1980 paper (the record
    ids use 1980). Ryabchikov 1964 and three Eichenauer papers have no
    title, and three sources were free-text strings instead of bib
    entries; their source files say `[title unknown]` with a note.
15. **Some values are computed from table columns.** Powell 1991
    (palladium) gives the measured concentration and the control
    pressure; HTM computes S = c / sqrt(p). That is now a transformation
    on the point file, which keeps both columns.

## 10. Migration

`htm migrate` (`records/migrate.py`, a one-off tool) does the automatic
part:

1. It imports the database in a subprocess with the property constructors
   wrapped, to learn where each property was created and its position in
   `htm.database`.
2. It reads each constructor call in the source. A call made only of
   numbers and units (including `np.exp(-6.53) * u.cm**2 / u.s`, energies
   written `965 * u.K * htm.k_B`, positional arguments and
   `(373, 473) * u.K` ranges) is written as a record, with the values as
   typed in the source rather than as pint converted them. Material
   entries and source files are created as needed (from the DOI, or from
   the `references.bib` entry when there is none). Each record says where
   it came from (`curation.migrated_from`) and carries a flag asking for a
   check against the paper.
3. Anything else goes to `data/migration/todo.md` with the reason.
4. `data/migration/legacy.yaml` maps every record id to the property it
   replaces in `htm.database`. The equivalence test checks each record
   against that exact property (class, source, isotope, material, values,
   range), not against a best match.

The tool is idempotent: rerunning it skips what is migrated and changes
nothing.

Data points are converted too when the temperatures and values are read
straight from loaded data (`1000 / data[:, 0] * u.K`,
`np.exp(data["y"]) * u.cm**2 / u.s`, `u.Quantity(data[:, 0], u.degC)`,
inline lists). The CSV written next to the record holds the values as
digitised (here 1000/T and ln D) and the axes say how to read them, so
nothing is converted before it is stored.

Module variables holding a quantity are inlined
(`data_T = u.Quantity([...], u.degC)`), unless they are modified in place
before use (`data_y *= density / molar_mass`), which is exactly where HTM
applied a conversion that needs a named transformation.

**Status: complete.** All 473 properties are records, with 50 materials
and 166 sources:

| How | Records |
|---|---|
| converted by `htm migrate` (literal values) | 281 |
| converted by `htm migrate` (data points) | 88 |
| transcribed by hand (conversions, derived properties, odd sources) | 104 |

All 473 reproduce the current database, including the fits of the data
points and the 14 derived properties, except the differences listed in
section 9 and in `tests/test_records.py`. The arithmetic HTM did on
published numbers is now named transformations with their parameters:
densities, molar masses and molar volumes, gas volume reference
temperatures, Sieverts constants, isotope scaling, reciprocals, and
concentrations divided by pressure. Hand-written records carry
`curation.migrated_from` too, so the manifest links every record to the
property it replaces.

Next:

1. Switch the library: build `htm.database` from the compiled records
   instead of `property_database/` (the compatibility layer already
   produces the same objects), keep both for one release with the
   equivalence test as the gate, then remove `property_database/`,
   `references.bib` (generated from `data/sources/`) and `htm migrate`.
2. Decide the open points of section 11, each as a labelled data change.
3. Verification sprint on W, 316L, Pb-17Li, EUROFER97 and FLiBe: every
   record starts as `draft` with a flag asking for a check against the
   paper.

## 11. Open points

1. Schumacher: find a Li50Pb50 density, or keep the Pb-17Li one as a
   labelled assumption.
2. Densities of liquids (Pb-17Li, lithium, FLiBe): evaluate a liquid
   correlation at the measurement temperature instead of a room
   temperature value. The transformations support it (`density_at`); it
   changes every affected solubility by 5 to 20%, so it should ship as its
   own labelled change.
3. Fauvet: confirm the diffusivity unit from the body of the paper.
4. Fit tolerance: is 10% over the measured range the right threshold
   before a curator has to choose between an author fit and the points?
5. Should `constant` records appear in `htm.diffusivities` at all, given
   they have no activation energy? They currently appear as an Arrhenius
   law with zero activation energy over a zero-width range.

Decided: the authors' fit is used unless it disagrees with the points
(section 3); the wheel ships the compiled JSON only and `htm` uses CODATA
constants (section 6); the Li molar mass is fixed (#318).
