User Guide
==========

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt

    # filter only tungsten and H
    diffusivities = htm.diffusivities.filter(material="tungsten").filter(isotope="h")

    htm.plotting.plot(diffusivities)


    plt.yscale("log")
    plt.ylabel("Diffusivity (m$^2$/s)")
    plt.legend()
    plt.show()

.. testcode::

    import h_transport_materials as htm

    import numpy as np

    # Create a custom property
    my_custom_property = htm.ArrheniusProperty(pre_exp=1e-5, act_energy=0.2)

    # From (T, y) data
    my_fitted_property = htm.ArrheniusProperty(
        data_T=[300, 400, 500, 600],
        data_y=[1e-8, 1e-7, 1e-6, 1e-5],
    )

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt

    tungsten_diffusivities = htm.diffusivities.filter(material="tungsten").filter(
        author=["moore", "zakharov"], exclude=True
    )

    # compute mean diffusivity
    mean_diffusivity = tungsten_diffusivities.mean()

    # plot
    htm.plotting.plot(tungsten_diffusivities, alpha=0.5)

    htm.plotting.plot(mean_diffusivity, color="black", linewidth=3)

    x_annotation = 0.0034
    plt.annotate("mean value", (x_annotation, mean_diffusivity.value(T=1 / x_annotation)))

    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
    plt.yscale("log")
    plt.show()
