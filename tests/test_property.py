import h_transport_materials as htm

def test_author_year_from_bib_source():
    source_bib = """@article{article-minimal,
        author = "L[eslie] B. Lamport",
        title = "The Gnats and Gnus Document Preparation System",
        journal = "G-Animal's Journal",
        year = "1986"
    }
    """
    my_prop = htm.Property(source=source_bib)

    assert my_prop.author == "lamport"
    assert my_prop.year == 1986

def test_author_year_from_bib_file():
    source_bib = "alberro_experimental_2015"
    my_prop = htm.Property(source=source_bib)

    assert my_prop.author == "alberro"
    assert my_prop.year == 2015