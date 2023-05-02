.. _plotting_user:

Plotting
========

Plotting a property
-------------------

HTM has a plotting module for visualising the temperature dependence of a property:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   D_1 = htm.Diffusivity(
      D_0=1 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.2* htm.ureg.eV * htm.ureg.particle**-1,
   )

   D_2 = htm.Diffusivity(
      D_0=2 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.3* htm.ureg.eV * htm.ureg.particle**-1,
   )

   plot(D_1)
   plot(D_2)

   plt.yscale("log")
   plt.show()


The matplotlib line parameters can be modified:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   D_1 = htm.Diffusivity(
      D_0=1 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.2* htm.ureg.eV * htm.ureg.particle**-1,
   )

   D_2 = htm.Diffusivity(
      D_0=2 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.3* htm.ureg.eV * htm.ureg.particle**-1,
   )

   plot(D_1, linestyle="-.", color="tab:red", linewidth=3, label="D1")
   plot(D_2, linestyle="dashed", color="tab:blue", linewidth=2, label="D2")

   plt.yscale("log")
   plt.legend()
   plt.show()

Plotting with experimental points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the (T,y) data is given with the attributes `.data_T` and `.data_y`, the experimental points are also plotted:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   S = htm.Solubility(
      data_T=[673, 773, 873, 973, 1073] * htm.ureg.K,
      data_y=[3e+21, 9e+20, 5e+20, 3e+20, 1e+20]
      * htm.ureg.particle
      * htm.ureg.m**-3
      * htm.ureg.Pa**-0.5,
   )

   plot(S)

   plt.yscale("log")
   plt.show()

In order to hide the experimental points, simply call:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   S = htm.Solubility(
      data_T=[673, 773, 873, 973, 1073] * htm.ureg.K,
      data_y=[3e+21, 9e+20, 5e+20, 3e+20, 1e+20]
      * htm.ureg.particle
      * htm.ureg.m**-3
      * htm.ureg.Pa**-0.5,
   )

   plot(S, show_datapoints=False)

   plt.yscale("log")
   plt.show()

Plotting groups of properties
-----------------------------

Alternatively, several properties can be plotted at once when part of a :class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>`:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   D_1 = htm.Diffusivity(
      D_0=1 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.2* htm.ureg.eV * htm.ureg.particle**-1,
   )

   D_2 = htm.Diffusivity(
      D_0=2 * htm.ureg.m**2 * htm.ureg.s**-1,
      E_D=0.3* htm.ureg.eV * htm.ureg.particle**-1,
   )

   plot(htm.PropertiesGroup([D_1, D_2]))

   plt.yscale("log")
   plt.show()

This means the entire database can be plotted in a few lines of code, here's an example for diffusivities:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   # filter only tungsten and H
   diffusivities = htm.diffusivities.filter(material="tungsten").filter(isotope="h")

   plot(diffusivities)

   plt.title("Tungsten diffusivity")
   plt.yscale("log")
   plt.legend()
   plt.show()


Calculate the mean value and plot it too:

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   # filter only tungsten and H
   diffusivities = htm.diffusivities.filter(material="tungsten")

   plot(diffusivities, alpha=0.5)
   plot(diffusivities.mean(), color="black", linewidth=3)

   plt.title("Tungsten diffusivity")
   plt.yscale("log")
   plt.show()

The properties can be coloured according to different attributes like ``materials``, ``author``...

.. plot::
   :include-source: true

   import h_transport_materials as htm
   from h_transport_materials.plotting import plot
   import matplotlib.pyplot as plt

   # filter only tungsten and H
   diffusivities = htm.diffusivities.filter(material="tungsten")

   plot(diffusivities, colour_by="author")

   plt.title("Tungsten diffusivity")
   plt.yscale("log")
   plt.show()

Interactive visualisation
-------------------------

For a more interactive visualisation of the HTM database, `visit the HTM-dashboard application <https://htm-dashboard-uan5l4xr6a-od.a.run.app/>`_.
