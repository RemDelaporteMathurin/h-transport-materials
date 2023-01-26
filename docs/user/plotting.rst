.. _plotting_user:

Plotting
========

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