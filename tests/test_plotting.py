import h_transport_materials as htm
import matplotlib.pyplot as plt
import pytest


def test_plot():
    """Simple test checking plot can be called"""
    my_prop = htm.ArrheniusProperty(
        1 * htm.ureg.dimensionless, 0.2 * htm.ureg.eV * htm.ureg.particle**-1
    )

    htm.plotting.plot(my_prop, alpha=0.2)
    plt.clf()


def test_plot_with_scatter():
    my_prop = htm.ArrheniusProperty(
        data_T=[500, 600, 700] * htm.ureg.K, data_y=[1, 2, 3] * htm.ureg.cm**2
    )

    htm.plotting.plot(my_prop, alpha=0.2, show_datapoints=True)
    plt.clf()

    htm.plotting.plot(
        my_prop, alpha=0.2, show_datapoints=True, inverse_temperature=False
    )
    plt.clf()


def test_plot_without_inverse_temp():
    my_prop = htm.ArrheniusProperty(
        1 * htm.ureg.dimensionless, 0.2 * htm.ureg.eV * htm.ureg.particle**-1
    )

    htm.plotting.plot(my_prop, alpha=0.2, inverse_temperature=False)
    plt.clf()


def test_plot_group():
    """Tests that a group can be plotted"""

    htm.plotting.plot(htm.diffusivities)
    plt.clf()


def test_plot_group_with_mixed_units():
    """Tests that plotting a group with mixed units raises an error"""
    with pytest.raises(ValueError):
        htm.plotting.plot(htm.solubilities)


def test_plot_group_with_colour_by():
    """Tests that a group can be plotted with a non-default colour_by argument"""

    htm.plotting.plot(htm.diffusivities, colour_by="material")
    plt.clf()


dict_mat = {
    htm.TUNGSTEN: "tab:grey",
    htm.COPPER: "tab:orange",
}
dict_isotope = {
    "H": "tab:grey",
    "D": "tab:orange",
    "T": "tab:blue",
}
dict_author = {
    "frauenfelder": "tab:grey",
}


@pytest.mark.parametrize(
    "colour_by,key_to_colour",
    [["material", dict_mat], ["isotope", dict_isotope], ["author", dict_author]],
)
def test_plot_group_with_key_to_colour_material(colour_by, key_to_colour):
    """Tests that a group can be plotted with a non-default colour_by argument and key_to_colour"""

    htm.plotting.plot(
        htm.diffusivities.filter(
            material=list(dict_mat.keys()), author=list(dict_author.keys())
        ),
        colour_by=colour_by,
        key_to_colour=key_to_colour,
    )
    plt.clf()


def test_warning_no_colour_by_and_key_to_colour():
    """Checks that a warning is raised when specifying key_to_colour with colour_by=property"""
    key_to_colour = {
        "H": "tab:grey",
        "D": "tab:orange",
        "T": "tab:blue",
    }
    with pytest.warns(UserWarning):
        htm.plotting.plot(htm.diffusivities, key_to_colour=key_to_colour)
        plt.clf()


@pytest.mark.parametrize(
    "colour_by",
    ["isotope", "material", "isotope", "author", "property"],
)
def test_plot_plotly_colour_by(colour_by):
    pytest.importorskip("plotly")
    htm.plotting.plot_plotly(htm.diffusivities, colour_by=colour_by)


@pytest.mark.parametrize(
    "group",
    [
        htm.diffusivities,
        htm.solubilities,
        htm.permeabilities,
        htm.recombination_coeffs,
        htm.dissociation_coeffs,
    ],
)
def test_plot_plotly_groups(group):
    pytest.importorskip("plotly")
    htm.plotting.plot_plotly(group)


@pytest.mark.filterwarnings("ignore:No property")
def test_plot_plotly_empty_group():
    pytest.importorskip("plotly")
    htm.plotting.plot_plotly(
        htm.diffusivities.filter(author="author_that_doesnt_exist")
    )


def test_plot_plotly_solubilities_only_one_unit():
    pytest.importorskip("plotly")
    htm.plotting.plot_plotly(htm.solubilities.filter(material=[htm.TUNGSTEN]))
