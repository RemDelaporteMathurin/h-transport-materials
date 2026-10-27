"""The ``htm`` command line tool.

    htm source add 10.1116/1.1492699     create data/sources/<key>.yaml from a DOI
    htm source sync                      add every DOI cited by a record but missing
    htm source from-bib refs.bib         sources without a DOI, from BibTeX
    htm build                            compile the records
    htm schema                           export JSON Schemas
    htm migrate                          convert property_database to records (one-off)
"""

import argparse
import os
import sys
from pathlib import Path

from . import build, schema, sources

SOURCES_DIR = build.DATA_DIR / "sources"
RECORDS_DIR = build.DATA_DIR / "records"
MATERIALS_DIR = build.DATA_DIR / "materials"


def _email(args):
    # Unpaywall needs a contact email; only used when given explicitly
    return args.email or os.environ.get("HTM_UNPAYWALL_EMAIL")


def _report(source, path, created):
    verb = "created" if created else "exists "
    print(f"{verb} {path.name}: {source.authors[0].family} {source.year}, {source.title}")


def source_add(args):
    for doi in args.doi:
        _report(*sources.add_doi(doi, args.sources, email=_email(args)))


def source_sync(args):
    known = {
        sources.normalize_doi(s.doi)
        for s in sources.existing_sources(args.sources).values()
        if s.doi
    }
    cited = sources.cited_dois(args.records, args.materials)
    missing = [cited[d] for d in sorted(set(cited) - known)]
    if not missing:
        print("all cited DOIs have a source file")
    for doi in missing:
        _report(*sources.add_doi(doi, args.sources, email=_email(args)))


def source_from_bib(args):
    existing = sources.existing_sources(args.sources)
    for source in sources.bibtex_to_sources(Path(args.file).read_text(encoding="utf-8"), existing):
        if source.doi:
            print(f"note: {source.key} has a DOI, prefer `htm source add {source.doi}`")
        _report(source, sources.write_source(source, args.sources), True)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["build"]:
        return build.main(argv[1:])
    if argv[:1] == ["schema"]:
        return schema.main(argv[1:])
    if argv[:1] == ["migrate"]:
        from . import migrate

        summary = migrate.run()
        print(
            f"{summary['written']} records written, {summary['records']} migrated in total,"
            f" {summary['hand']} left for hand transcription (data/migration/todo.md)."
        )
        if summary["materials_created"]:
            print("materials created:", ", ".join(summary["materials_created"]))
        return None

    parser = argparse.ArgumentParser(prog="htm", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="group", required=True)
    sub.add_parser("build", help="compile the records (see htm build --help)")
    sub.add_parser("schema", help="export JSON Schemas (see htm schema --help)")
    sub.add_parser("migrate", help="convert property_database to records (one-off)")
    src = sub.add_parser("source", help="manage source files").add_subparsers(
        dest="command", required=True
    )

    def common(p):
        p.add_argument("--sources", type=Path, default=SOURCES_DIR)
        p.add_argument("--email", help="contact email for the Unpaywall open access lookup")
        return p

    common(src.add_parser("add", help="from one or more DOIs")).add_argument("doi", nargs="+")
    sync = common(src.add_parser("sync", help="add DOIs cited by records and materials"))
    sync.add_argument("--records", type=Path, default=RECORDS_DIR)
    sync.add_argument("--materials", type=Path, default=MATERIALS_DIR)
    common(src.add_parser("from-bib", help="from a BibTeX file")).add_argument("file")

    args = parser.parse_args(argv)
    {"add": source_add, "sync": source_sync, "from-bib": source_from_bib}[args.command](args)


if __name__ == "__main__":
    main()
