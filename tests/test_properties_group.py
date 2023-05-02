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
    mean_prop = my_group.mean()

    # test
    assert mean_prop.pre_exp.magnitude == pytest.approx(mean_D_0, rel=0.2)
    assert mean_prop.act_energy.magnitude == pytest.approx(mean_E_D, rel=0.2)


def test_mean_is_type_arrhenius_property():
    my_prop = htm.ArrheniusProperty(
        0.1 * htm.ureg.dimensionless, 0.1 * htm.ureg.eV * htm.ureg.particle**-1
    )
    my_group = htm.PropertiesGroup([my_prop])

    assert isinstance(my_group.mean(), htm.ArrheniusProperty)


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

    for prop_file, prop_ref in zip(data_in["data"], my_group):
        for key, val in prop_file.items():
            if hasattr(prop_ref, key):
                if key == "units":
                    assert f"{getattr(prop_ref, key):~}" == val
                elif key in ["pre_exp", "act_energy"]:
                    assert getattr(prop_ref, key).magnitude == val["value"]
                elif key in ["data_T", "data_y"]:
                    assert np.array_equal(
                        getattr(prop_ref, key).magnitude, val["value"]
                    )
                elif key == "range":
                    prop_range = getattr(prop_ref, key)
                    assert [
                        prop_range[0].magnitude,
                        prop_range[1].magnitude,
                    ] == val["value"]
                else:
                    assert getattr(prop_ref, key) == val


def test_filter_warns_when_no_props():
    with pytest.warns(UserWarning):
        htm.diffusivities.filter(material="material_that_doesn_not_exist")


def test_units_property():
    """Checks the units property returns the expected value"""
    diff = htm.Diffusivity(
        D_0=1 * htm.ureg.m**2 * htm.ureg.s**-1,
        E_D=0.1 * htm.ureg.eV * htm.ureg.particle**-1,
    )
    sol = htm.Solubility(
        S_0=1 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-1,
        E_S=0.1 * htm.ureg.eV * htm.ureg.particle**-1,
    )

    assert (
        htm.PropertiesGroup([sol, sol]).units
        == htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-1
    )
    assert htm.PropertiesGroup([diff, diff]).units == htm.ureg.m**2 * htm.ureg.s**-1
    assert htm.PropertiesGroup([sol, diff]).units == "mixed units"


def test_to_latex_table():
    htm.diffusivities.to_latex_table()


def test_mean_has_units():
    assert htm.diffusivities.mean().units == htm.ureg.m**2 * htm.ureg.s**-1


def test_cannot_compute_mean_on_mixed_groups():
    prop1 = htm.ArrheniusProperty(
        0.1 * htm.ureg.dimensionless, 0.1 * htm.ureg.eV * htm.ureg.particle**-1
    )
    prop2 = htm.ArrheniusProperty(
        0.1 * htm.ureg.m, 0.1 * htm.ureg.eV * htm.ureg.particle**-1
    )
    my_group = htm.PropertiesGroup([prop1, prop2])

    with pytest.raises(ValueError, match="Can't compute mean on mixed units groups"):
        my_group.mean()
