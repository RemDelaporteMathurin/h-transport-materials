from multiprocessing.sharedctypes import Value
import h_transport_materials as htm

from pybtex.database import BibliographyData
import pytest


source_bib_as_string = """@article{article-minimal,
    author = "L[eslie] B. Lamport",
    title = "The Gnats and Gnus Document Preparation System",
    journal = "G-Animal's Journal",
    year = "1986"
}
"""

source_bib_from_file = "alberro_experimental_2015"


def test_author_year_from_bib_source():
    my_prop = htm.Property(source=source_bib_as_string)

    assert my_prop.author == "lamport"
    assert my_prop.year == 1986


def test_author_year_from_bib_file():
    my_prop = htm.Property(source=source_bib_from_file)

    assert my_prop.author == "alberro"
    assert my_prop.year == 2015


@pytest.mark.parametrize("source", [source_bib_as_string, source_bib_from_file])
def test_bibdata(source):
    my_prop = htm.Property(source=source)

    assert isinstance(my_prop.bibdata, BibliographyData)


def test_bibdata_raises_error_when_bibsource_is_none():
    my_prop = htm.Property(source="coucou")
    with pytest.raises(ValueError, match="No bibsource found"):
        my_prop.bibdata


def test_export_bib():
    my_prop = htm.Property(source=source_bib_as_string)
    my_prop.export_bib("out.bib")


def test_warning_overwriting_author():
    with pytest.warns(
        UserWarning,
        match="author argument will be ignored since a bib source was found",
    ):
        htm.Property(source=source_bib_as_string, author="me")


def test_warning_overwriting_year():
    with pytest.warns(
        UserWarning,
        match="year argument will be ignored since a bib source was found",
    ):
        htm.Property(source=source_bib_as_string, year=2010)


def test_nb_citations():
    my_prop = htm.Property(source=source_bib_from_file)
    assert my_prop.nb_citations > 0


def test_nb_citations_no_citations_with_unknown_source():
    my_prop = htm.Property(source="coucou")

    assert my_prop.nb_citations == 0


def test_range_cannot_be_negative():
    with pytest.raises(ValueError, match="range must be stricly positive"):
        htm.Property(range=(-1, 2))
    with pytest.raises(ValueError, match="range must be stricly positive"):
        htm.Property(range=(0, 2))


def test_has_doi():
    """Checks that Property has a doi attribute"""
    prop = htm.Property(source=source_bib_from_file)
    assert prop.doi
