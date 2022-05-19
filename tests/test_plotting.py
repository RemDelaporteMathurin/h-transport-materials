import h_transport_materials as htm


def test_plot():
    """Simple test checking plot can be called"""
    my_prop = htm.ArrheniusProperty(1, 0.2)

    htm.plotting.plot(my_prop, alpha=0.2)
