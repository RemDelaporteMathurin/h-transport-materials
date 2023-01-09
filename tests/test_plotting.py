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
