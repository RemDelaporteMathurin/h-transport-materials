"""Creates source files from a DOI (or a BibTeX entry for grey literature).

Metadata is fetched once from doi.org (CSL-JSON content negotiation, works
for Crossref and DataCite DOIs), cleaned, and written to
``data/sources/<key>.yaml``. The file is committed so builds stay offline
and metadata errors can be corrected and reviewed.
"""

import html
import json
import re
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from .doi import normalize_doi, strip_doi  # noqa: F401  re-exported
from .models import Source

USER_AGENT = "h-transport-materials (https://github.com/RemDelaporteMathurin/h-transport-materials)"

CSL_TYPES = {
    "journal-article": "article",
    "article": "article",
    "article-journal": "article",
    "report": "report",
    "thesis": "thesis",
    "dissertation": "thesis",
    "book": "book",
    "edited-book": "book",
    "monograph": "book",
    "chapter": "chapter",
    "book-chapter": "chapter",
    "paper-conference": "conference",
    "proceedings-article": "conference",
}

BIBTEX_TYPES = {
    "article": "article",
    "techreport": "report",
    "report": "report",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "thesis": "thesis",
    "book": "book",
    "incollection": "chapter",
    "inbook": "chapter",
    "inproceedings": "conference",
    "conference": "conference",
}

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−"), "-")


def clean_given(given: str | None) -> str | None:
    """'G.A' or 'GA' -> 'G. A.' for initials-only given names, else unchanged"""
    given = clean_text(given)
    if given and re.fullmatch(r"(?:[A-Z]\.?[\s-]?)+", given):
        return " ".join(f"{c}." for c in re.findall(r"[A-Z]", given))
    return given


def clean_text(text: str | None) -> str | None:
    """Removes markup and typographic oddities from fetched metadata"""
    if text is None:
        return None
    if isinstance(text, list):
        text = text[0] if text else ""
    text = re.sub(r"<[^>]+>", "", html.unescape(text))  # <i>, <sub>, jats tags
    text = re.sub(r"(?<!\\)[{}]", "", text)  # bibtex case-protecting braces
    text = text.translate(_DASHES).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip() or None


def make_key(family: str, year: int, taken=()) -> str:
    """frauenfelder1969, then frauenfelder1969b, ... if already taken"""
    ascii_name = unicodedata.normalize("NFKD", family).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z]", "", ascii_name.lower()) + str(year)
    key, suffix = base, ord("b")
    while key in taken:
        key, suffix = base + chr(suffix), suffix + 1
    return key


def fetch_csl(doi: str, timeout=20) -> dict:
    """Fetches CSL-JSON metadata for a DOI from doi.org"""
    url = "https://doi.org/" + urllib.parse.quote(normalize_doi(doi), safe="/")
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.citationstyles.csl+json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_open_access_url(doi: str, email: str, timeout=20) -> str | None:
    """Best open access URL from Unpaywall (needs a contact email), or None"""
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(normalize_doi(doi), safe='/')}?email={urllib.parse.quote(email)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        best = json.loads(r.read().decode("utf-8")).get("best_oa_location") or {}
    return best.get("url")


def _orcid(author):
    orcid = author.get("ORCID")
    return orcid.rstrip("/").split("/")[-1] if orcid else None


def _people(entries):
    return [
        {
            "family": clean_text(a.get("family") or a.get("literal")),
            "given": clean_given(a.get("given")),
            "orcid": _orcid(a),
        }
        for a in entries
        if a.get("family") or a.get("literal")
    ]


def csl_to_source(csl: dict, taken=()) -> Source:
    """Converts CSL-JSON into a Source, deriving the key from the first author
    (or editor, for edited books) and the year"""
    authors = _people(csl.get("author", []))
    editors = [] if authors else _people(csl.get("editor", []))
    if not authors and not editors:
        raise ValueError("no authors or editors in the metadata, write the source by hand")
    date = csl.get("issued") or csl.get("published-print") or csl.get("published-online")
    year = int(date["date-parts"][0][0])
    return Source(
        key=make_key((authors or editors)[0]["family"], year, taken),
        type=CSL_TYPES.get(csl.get("type"), "other"),
        title=clean_text(csl.get("title")),
        authors=authors,
        editors=editors,
        year=year,
        journal=clean_text(csl.get("container-title")),
        volume=clean_text(str(csl["volume"])) if csl.get("volume") else None,
        issue=clean_text(str(csl["issue"])) if csl.get("issue") else None,
        pages=clean_text(csl.get("page") or csl.get("article-number")),
        doi=strip_doi(csl["DOI"]) if csl.get("DOI") else None,
        url=_url(csl),
    )


def _url(csl):
    """The URL unless it only points back to the DOI"""
    url = csl.get("URL")
    if url and csl.get("DOI") and normalize_doi(url) == normalize_doi(csl["DOI"]):
        return None
    return url


def bibtex_to_sources(text: str, taken=()) -> list[Source]:
    """Converts BibTeX entries (e.g. exported from Zotero) into Sources"""
    from pybtex.database import parse_string

    sources, taken = [], set(taken)
    for entry in parse_string(text, bib_format="bibtex").entries.values():
        f = entry.fields
        persons = entry.persons.get("author", [])
        authors = [
            {
                "family": clean_text(" ".join(p.prelast_names + p.last_names)),
                "given": clean_given(" ".join(p.first_names + p.middle_names)) or None,
            }
            for p in persons
        ]
        if not authors:
            raise ValueError(f"{entry.key}: no authors")
        year = int(f["year"])
        source = Source(
            key=make_key(authors[0]["family"], year, taken),
            type=BIBTEX_TYPES.get(entry.type.lower(), "other"),
            title=clean_text(f.get("title")),
            authors=authors,
            year=year,
            journal=clean_text(f.get("journal") or f.get("booktitle") or f.get("institution") or f.get("school")),
            volume=clean_text(f.get("volume")),
            issue=clean_text(f.get("number")),
            pages=clean_text(f.get("pages")),
            doi=strip_doi(f["doi"]) if f.get("doi") else None,
            url=f.get("url"),
        )
        taken.add(source.key)
        sources.append(source)
    return sources


def existing_sources(sources_dir) -> dict:
    """Returns key -> Source for the source files already in sources_dir"""
    out = {}
    for path in Path(sources_dir).glob("*.yaml"):
        with open(path, encoding="utf-8") as f:
            s = Source(**yaml.safe_load(f))
        out[s.key] = s
    return out


def write_source(source: Source, sources_dir) -> Path:
    path = Path(sources_dir) / f"{source.key}.yaml"
    data = source.model_dump(mode="json", exclude_none=True)
    data["authors"] = [{k: v for k, v in a.items() if v is not None} for a in data["authors"]]
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=100)
    return path


def add_doi(doi, sources_dir, email=None, fetch=fetch_csl):
    """Creates the source file for a DOI unless one exists.

    Returns:
        tuple: (Source, Path, created)
    """
    existing = existing_sources(sources_dir)
    as_cited, doi = strip_doi(doi), normalize_doi(doi)
    for s in existing.values():
        if s.doi and normalize_doi(s.doi) == doi:
            return s, Path(sources_dir) / f"{s.key}.yaml", False
    source = csl_to_source(fetch(doi), taken=existing)
    if source.doi and normalize_doi(source.doi) == doi:
        source.doi = as_cited  # doi.org sometimes returns DOIs lowercased
    if email:
        source.open_access_url = fetch_open_access_url(doi, email)
    return source, write_source(source, sources_dir), True


def _source_dois(node):
    """DOIs in every ``source: {doi: ...}`` block of a loaded YAML document"""
    if isinstance(node, dict):
        source = node.get("source")
        if isinstance(source, dict) and source.get("doi"):
            yield source["doi"]
        for value in node.values():
            yield from _source_dois(value)
    elif isinstance(node, list):
        for value in node:
            yield from _source_dois(value)


def cited_dois(*dirs) -> dict:
    """DOIs cited by records or materials (any source.doi), as normalized DOI -> DOI as cited"""
    dois = {}
    for directory in dirs:
        for path in sorted(Path(directory).glob("*.yaml")):
            with open(path, encoding="utf-8") as f:
                for doi in _source_dois(yaml.safe_load(f)):
                    dois.setdefault(normalize_doi(doi), strip_doi(doi))
    return dois
