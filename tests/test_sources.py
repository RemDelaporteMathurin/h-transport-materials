"""Tests for creating source files from DOIs and BibTeX (no network needed)."""

import pytest

pytest.importorskip("pydantic")
pytest.importorskip("yaml")

import yaml

from h_transport_materials.records import build, cli, sources

# CSL-JSON as doi.org returns it, with the usual oddities
ELSEVIER_CSL = {
    "type": "journal-article",
    "title": "Hydrogen isotope diffusive transport parameters in <i>pure</i> polycrystalline tungsten",
    "author": [
        {"family": "Esteban", "given": "G.A"},
        {"family": "Perujo", "given": "A", "ORCID": "http://orcid.org/0000-0002-1825-0097"},
    ],
    "container-title": "Journal of Nuclear Materials",
    "volume": "295",
    "issue": "1",
    "page": "49–56",
    "issued": {"date-parts": [[2001, 5]]},
    "DOI": "10.1016/s0022-3115(01)00486-x",
    "URL": "http://dx.doi.org/10.1016/s0022-3115(01)00486-x",
}

AIP_CSL = {
    "type": "journal-article",
    "title": "Lithium‐Lead alloys",
    "author": [{"family": "Müller", "given": "Jörg"}],
    "container-title": "Journal of Applied Physics",
    "article-number": "113531",
    "issued": {"date-parts": [[2010]]},
    "DOI": "10.1063/1.3386515",
}


def test_csl_cleanup():
    s = sources.csl_to_source(ELSEVIER_CSL)
    assert s.key == "esteban2001"
    assert s.title == "Hydrogen isotope diffusive transport parameters in pure polycrystalline tungsten"
    assert [a.given for a in s.authors] == ["G. A.", "A."]
    assert s.authors[1].orcid == "0000-0002-1825-0097"
    assert s.pages == "49-56"
    assert s.url is None  # only pointed back to the DOI


def test_csl_article_number_and_unicode():
    s = sources.csl_to_source(AIP_CSL)
    assert s.pages == "113531"
    assert s.title == "Lithium-Lead alloys"
    assert s.key == "muller2010"
    assert s.authors[0].family == "Müller"  # kept as is, only the key is ascii


def test_key_collision():
    assert sources.make_key("Esteban", 2001, {"esteban2001"}) == "esteban2001b"
    assert sources.make_key("Esteban", 2001, {"esteban2001", "esteban2001b"}) == "esteban2001c"


@pytest.mark.parametrize(
    "doi",
    ["10.1116/1.1492699", "https://doi.org/10.1116/1.1492699", "doi:10.1116/1.1492699", "10.1116/1.1492699 "],
)
def test_normalize_doi(doi):
    assert sources.normalize_doi(doi) == "10.1116/1.1492699"


def test_add_doi_keeps_cited_case_and_is_idempotent(tmp_path):
    calls = []

    def fake_fetch(doi):
        calls.append(doi)
        return ELSEVIER_CSL

    s, path, created = sources.add_doi("10.1016/S0022-3115(01)00486-X", tmp_path, fetch=fake_fetch)
    assert created and path.name == "esteban2001.yaml"
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["doi"] == "10.1016/S0022-3115(01)00486-X"

    _, _, created = sources.add_doi("https://doi.org/10.1016/s0022-3115(01)00486-x", tmp_path, fetch=fake_fetch)
    assert not created
    assert len(calls) == 1


def test_bibtex_import(tmp_path):
    bib = r"""
    @techreport{whatever,
      title = {Hydrogen in {Pb-17Li}: a {KIT} report},
      author = {Reiter, F. and Smith, John},
      institution = {Karlsruhe Institute of Technology},
      year = {1991},
    }
    """
    (s,) = sources.bibtex_to_sources(bib, taken={"reiter1991"})
    assert s.key == "reiter1991b"
    assert s.type == "report"
    assert s.title == "Hydrogen in Pb-17Li: a KIT report"
    assert [a.family for a in s.authors] == ["Reiter", "Smith"]
    assert s.journal == "Karlsruhe Institute of Technology"
    sources.write_source(s, tmp_path)
    assert (tmp_path / "reiter1991b.yaml").exists()


def test_generated_source_files_are_valid():
    """The committed source files load and match the DOIs records cite"""
    existing = sources.existing_sources(build.DATA_DIR / "sources")
    known = {sources.normalize_doi(s.doi) for s in existing.values() if s.doi}
    assert set(sources.cited_dois(build.DATA_DIR / "records")) <= known


def test_sync_reports_nothing_missing(capsys):
    cli.main(["source", "sync"])
    assert "all cited DOIs have a source file" in capsys.readouterr().out


def test_build_asks_for_missing_source(tmp_path):
    import shutil

    data = tmp_path / "data"
    shutil.copytree(build.DATA_DIR, data)
    (data / "sources" / "heinola2010.yaml").unlink()
    with pytest.raises(build.BuildError, match="htm source add 10.1063/1.3386515"):
        build.build(data)
