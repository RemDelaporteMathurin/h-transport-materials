# CLAUDE.md

Guidance for working in h-transport-materials (HTM), a database of hydrogen
transport properties (diffusivity, solubility, permeability, recombination and
dissociation coefficients) with a Python library to query, convert and plot them.

## Working with the maintainer (Rémi)

- No em dashes in prose for him (docs, READMEs, PR text, commit messages): use
  colons, semicolons or rephrase.
- Never put Claude session links in commit messages or PR descriptions.
- Commit, push or open PRs only when asked. Never force-push a branch with an
  open PR: merge `main` into it instead of rebasing.
- FESTIM (also maintained by Rémi) is the downstream user that matters most.
  Do not break `htm.diffusivities.filter(...)`-style scripts.
- Any change to published values needs his go-ahead and must be listed (which
  records, by how much, why) in the commit and the PR.

## Philosophy

HTM exists to stop errors propagating from papers to users:

1. Store what the paper prints: values, units, form of the law.
2. Everything HTM does to the data is a named transformation with parameters,
   a rationale and an origin (`paper` or `htm`). HTM's own choices are listed
   next to the value (`htm_assumptions`).
3. Every record cites a source, ideally a DOI and a location in the paper.

When in doubt, flag it in the record (`curation.flags`) rather than guess.
Never invent a title, range, unit or value that is not in the source.

## Layout

```
h_transport_materials/          the library
  property.py, properties_group.py, material.py, plotting.py
  property_database/            legacy Python records (being replaced)
  records/                      the record format
    models.py                   pydantic schema (Record, Material, Source, ...)
    transforms.py               named transformations (registry)
    build.py                    YAML -> validated -> normalised JSON
    compat.py                   built records -> existing property objects
    loader.py                   reads the compiled JSON (no pydantic needed)
    sources.py, doi.py          source files from DOIs or BibTeX
    migrate.py                  one-off property_database -> YAML tool
    contribute.py               issue forms -> record files (the contribution bot)
    report.py                   record report (plots, checks) commented on PRs
    cli.py                      the `htm` command
data/
  records/<id>.yaml (+ .csv)    one record per source x property x isotope x material
  materials/<id>.yaml           material registry (composition, density, ...)
  sources/<key>.yaml            generated from DOIs, committed
  elements.yaml                 atomic weights used for molar masses
  migration/legacy.yaml         record id -> index in htm.legacy_database()
  migration/todo.md             properties still to transcribe (empty when done)
docs/rfc/0001-data-records.md   design, findings and open points
example_records.ipynb           tour of the records (on feat/records-database)
```

Record ids: `htm:<MAT>-<D|S|P|Kr|Kd>-<H|D|T>-<author><year>[-b]`, e.g.
`htm:W-D-H-frauenfelder1969`. The file name is the id without `htm:`. Ids are
permanent.

## Commands

```bash
pip install -e ".[tests,plotly,build]"

pytest                                   # whole suite (about 2 min)
pytest tests/test_records.py -k equivalence

htm build --out dist/htm-data.json       # compile data/ (also: python -m h_transport_materials.records.build)
htm schema --out dist/schema             # JSON Schemas
htm source add <DOI>                     # create data/sources/<key>.yaml from doi.org
htm source sync                          # add every DOI cited by a record or material
htm source from-bib refs.bib             # sources without a DOI
htm migrate                              # rerun the migration (idempotent)
htm contribute form                      # regenerate .github/ISSUE_TEMPLATE/{new,change}-record.yml
htm contribute from-issue issue.json --dry-run   # what the bot does with an issue (REST API JSON)
htm report --base a.json --head b.json --plots plots/   # the record report posted on PRs

flake8 h_transport_materials/records --max-line-length=127
```

CI tests Python 3.11 with pint 0.24.4 and Python 3.14 with the latest pint,
and builds a wheel to check it ships the compiled JSON and reads it without
pydantic or pyyaml.

## Adding or changing data

- Cite the source by DOI in the record; `htm source sync` creates the source
  file. Correct bad publisher metadata by editing the source file.
- Material properties (density, composition) go in `data/materials/`, not in
  records. Transformations look them up (`density_from`, `density_at`,
  `molar_mass_from`) or take explicit values the paper gives.
- Data points: a CSV next to the record, holding the values as digitised (e.g.
  1000/T and ln y), with axes saying how to read them. Do not convert first.
- A paper's own fit goes in `reported.author_fit`. The build compares it with a
  fit of the points; above 10% disagreement a curator must set
  `reported.selected` with a `selection_note`.
- Properties computed from other records use `form: derived`.
- After editing records, run the equivalence test. A record that intentionally
  differs from the legacy database must be listed in `EXPECTED_DIFFERENCES` in
  `tests/test_records.py` with the reason and the expected size.

## Contributions through issues

- The explorer's buttons open the issue forms `new-record.yml` and
  `change-record.yml`, prefilled through the URL (`contribute.prefill_new`,
  `prefill_change`). The forms are generated from `contribute.py`: edit it,
  then run `htm contribute form`. A test fails if they drift, including when
  a material is added to `data/materials`.
- `.github/workflows/contribute.yml` (must be on `main`: issue events run from
  the default branch) runs `htm contribute from-issue` and opens a PR from
  `contrib/issue-<N>` into `HTM_RECORDS_BRANCH`. It uses a GitHub App token
  (`HTM_BOT_APP_ID`, `HTM_BOT_PRIVATE_KEY`) so CI runs on its PRs. Editing the
  issue adds a commit to the same PR.
- `.github/workflows/record-report.yml` comments on every PR touching `data/`;
  plots go to the orphan branch `bot-assets`.
- Contributed records are not in `data/migration/legacy.yaml`; the
  equivalence test skips them. Changing a migrated record's values still
  needs an `EXPECTED_DIFFERENCES` entry.
- "Closes #N" only closes the issue when merging into the default branch:
  close it by hand while the bot targets `feat/records-database`.

## Gotchas

- pint 0.26 raises `OffsetUnitCalculusError` on `array * u.degC`. Use
  `u.Quantity(array, u.degC)`.
- numpy 2: `repr(np.float64(x))` is `np.float64(x)`. Convert to `float` before
  writing CSV files, or every value reads back as NaN.
- `references.bib` has errors: untitled entries, a wrong year (Begun, 2008 for
  a 1980 paper), free-text citations. Source files say `[title unknown]` with
  a note rather than inventing anything.
- Windows: the scratchpad path is long; pip installs of packages with deep
  paths (jedi, the HTM wheel itself) fail there. Use a short path such as
  `C:\Users\rdela\htmtmp` for temporary environments and delete it after.
- `sed -i` with a line number is fragile after earlier edits shift lines;
  prefer the Edit tool or match on content.
- `htm.k_B`, `htm.Rg` and `htm.avogadro_nb` are CODATA values from
  `scipy.constants`. The records build uses them too, so equivalence holds.

## Branches (October 2026)

- `main`: released library (0.18.4) with the legacy Python database.
- `feat/overhaul-records-prototype` (PR #317): the record format, tooling,
  migrated data and the RFC. Does not change `htm.database`.
- `feat/records-database`: builds `htm.database` from the records, for
  testing. `htm.legacy_database()` and `HTM_LEGACY_DATABASE=1` give the old
  database. Installing from git does not work yet (the compiled JSON is only
  generated by the release workflow); use a clone with `pip install -e ".[build]"`.
