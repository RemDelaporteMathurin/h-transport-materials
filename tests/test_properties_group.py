import h_transport_materials as htm
import numpy as np
import json
import pytest
from pybtex.database import BibliographyData


def test_iterable():
    """Checks that PropertiesGroup can be iterated through"""
    my_group = htm.PropertiesGroup(htm.Property() for _ in range(10))

    for prop in my_group:
        assert isinstance(prop, htm.Property)


def test_adding_two_groups():
    """Checks two groups can be added"""
    my_group1 = htm.PropertiesGroup(htm.Property() for _ in range(10))
    my_group2 = htm.PropertiesGroup(htm.Property() for _ in range(10))

    sum_of_groups = my_group1 + my_group2
    assert len(sum_of_groups) == len(my_group1) + len(my_group2)


def test_filter_author_lower_case():
    """Checks that PropertiesGroup can filter authors even
    if the attributes are not lowercase"""

    my_prop = htm.Property(author="ReM")

    my_group = htm.PropertiesGroup([my_prop])

    filtered_group = my_group.filter(author="rem")

    assert filtered_group[0] == my_prop


def test_filter_isotope_lower_case():
    """Checks that PropertiesGroup can filter isotopes even
    if the attributes are not lowercase"""

    my_prop = htm.Property(isotope="H")

    my_group = htm.PropertiesGroup([my_prop])

    filtered_group = my_group.filter(isotope="h")

    assert filtered_group[0] == my_prop


@pytest.mark.parametrize(
    "mean_D_0,mean_E_D",
    [
        (D_0, E_D)
        for D_0 in np.linspace(2, 60, num=3)
        for E_D in np.linspace(0.1, 3, num=3)
    ],
)
def test_mean(mean_D_0, mean_E_D):
    """Creates a PropertiesGroup object with a list of properties that
    have their activation energy and pre-exponential factor varying
    around mean values. The method .mean() is called and the computed
    mean values are compared with the theoretical ones.

    Args:
        mean_D_0 (float): mean pre-exponential factor
        mean_E_D (float): mean activation energy
    """
    # build
    my_group = htm.PropertiesGroup()
    nb_props = 30

    noise_D_0 = np.random.normal(0, mean_D_0 / 10, nb_props)
    noise_E_D = np.random.normal(0, mean_E_D / 10, nb_props)

    # create properties with noise
    for i in range(nb_props):
        my_group.append(
            htm.ArrheniusProperty(
                pre_exp=(mean_D_0 + noise_D_0[i]) * htm.ureg.m**2 * htm.ureg.s**-1,
                act_energy=(mean_E_D + noise_E_D[i])
                * htm.ureg.eV
                * htm.ureg.particle**-1,
            )
        )

    # run
    mean_D_0_computed, mean_E_D_computed = my_group.mean()

    # test
    assert mean_D_0_computed == pytest.approx(mean_D_0, rel=0.2)
    assert mean_E_D_computed == pytest.approx(mean_E_D, rel=0.2)


def test_bibdata():
    source_bib = """@article{article-minimal,
        author = "L[eslie] B. Lamport",
        title = "The Gnats and Gnus Document Preparation System",
        journal = "G-Animal's Journal",
        year = "1986"
    }
    """

    my_group = htm.PropertiesGroup(
        [
            htm.Property(material="my_mat", source=source_bib),
            htm.Property(material="my_mat", source="source"),
        ]
    )

    assert isinstance(my_group.bibdata, BibliographyData)


def test_export_bib():
    source_bib = """@article{article-minimal,
        author = "L[eslie] B. Lamport",
        title = "The Gnats and Gnus Document Preparation System",
        journal = "G-Animal's Journal",
        year = "1986"
    }
    """

    my_group = htm.PropertiesGroup(
        [
            htm.Property(material="my_mat", source=source_bib),
            htm.Property(material="my_mat", source="source"),
        ]
    )
    my_group.export_bib("out.bib")


def test_export_to_json():
    # build

    my_group = htm.database

    # run

    my_group.export_to_json("out.json")

    # test
    with open("out.json") as json_file:
        data_in = json.load(json_file)

    for prop_file, prop_ref in zip(data_in, my_group):
        for key, val in prop_file.items():
            if hasattr(prop_ref, key):
                if isinstance(val, list):
                    for item1, item2 in zip(val, getattr(prop_ref, key)):
                        assert item1 == item2
                else:
                    if key == "units":
                        assert f"{getattr(prop_ref, key):~}" == val
                    else:
                        assert getattr(prop_ref, key) == val
