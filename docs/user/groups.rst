Properties Groups
=================

Creating groups
---------------

Properties can be grouped using the :class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>` class.

.. testcode::

    import h_transport_materials as htm

    prop1 = htm.Diffusivity(1, 0)
    prop2 = htm.Diffusivity(2, 0)
    
    my_group = htm.PropertiesGroup([prop1, prop2])


:class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>` inherits from ``list``.
Groups can therefore be concatenated:

.. testcode::

    group1 = htm.PropertiesGroup([prop1, prop2])
    group2 = htm.PropertiesGroup([prop1, prop2])

    big_group = group1 + group2

And iterated through:

.. testcode::

    for prop in group1:
        pass

HTM database
------------

HTM already contains several hundreds of properties stored in ``database``.

.. testcode::

    from h_transport_materials import database
    nb_properties = len(database)

``database`` contains all the properties.
Users can also access all the diffusivities in ``diffusivities``.
``solubilities``, ``permeabilities``, ``recombination_coeffs``, and ``dissociation_coeffs`` are also available.

.. _filtering:

Filters
-------

Property groups can be filtered by several property attributes: ``materials``, ``author``, ``year``...

.. testcode::

    import h_transport_materials as htm

    prop1 = htm.Diffusivity(1, 0, author="jack")
    prop2 = htm.Diffusivity(2, 0, author="jon")
    prop3 = htm.Diffusivity(3, 0, author="jean")
    
    group = htm.PropertiesGroup([prop1, prop2, prop3])

    # filtered groups
    only_jack = group.filter(author="jack")
    jon_and_jean = group.filter(author=["jon", "jean"])

    everyone_but_jon = group.filter(author="jon", exclude=True)

The internal database being a :class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>` too, it can also be filtered:
For instance, to filter the tungsten diffusivities of HTM:

.. testcode::

    import h_transport_materials as htm

    tungsten_diffusivities = htm.diffusivities.filter(material=htm.TUNGSTEN)

To filter all the steel alloys, two options. Explicitely filter each grade of steel:

.. testcode::

    steels = [htm.STEEL_RAFM, htm.STEEL_316L, htm.STEEL_SERIES_300]

    steel_diffusivities = htm.diffusivities.filter(material=steels)


Filter with the :class:`Material <h_transport_materials.material.Material>` object ``htm.Steel``:

.. testcode::

    steel_diffusivities = htm.diffusivities.filter(material=htm.Steel)

Alternatively, the properties can be filtered by the material name as a string:

.. testcode::

    steel_diffusivities = htm.diffusivities.filter(material="steel")
    tungsten_diffusivities = htm.diffusivities.filter(material="tungsten")

Computing mean property
-----------------------

With :class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>` objects, it is possible to compute the mean property using the :meth:`~h_transport_materials.properties_group.PropertiesGroup.mean` method.

.. testcode::

    import h_transport_materials as htm

    prop1 = htm.Diffusivity(1, 0.1)
    prop2 = htm.Diffusivity(2, 0.2)
    
    group = htm.PropertiesGroup([prop1, prop2])
    mean_property = group.mean()

    print(mean_property)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    Author:
    Material:
    Year: None
    Isotope: None
    Pre-exponential factor: 1.41×10⁰ m²/s
    Activation energy: 1.50×10⁻¹ eV/particle

.. plot::
   :include-source: false

    import h_transport_materials as htm
    from h_transport_materials.plotting import plot
    import matplotlib.pyplot as plt

    prop1 = htm.Diffusivity(1, 0.1)
    prop2 = htm.Diffusivity(2, 0.2)
    
    group = htm.PropertiesGroup([prop1, prop2])
    mean_property = group.mean()

    plot(group, alpha=0.5)
    plot(mean_property, color="black")

    plt.annotate("mean property", (0.0025, 2e-2))
    plt.yscale("log")
    plt.xlabel("1/T (K$^{-1}$)")
    plt.show()

Export group
------------

It is possible to export a :class:`PropertiesGroup() <h_transport_materials.properties_group.PropertiesGroup>` to JSON by running:

.. testcode::

    steel_diffusivities = htm.diffusivities.filter(material=htm.Steel)

    steel_diffusivities.export_to_json("filename.json")

It is also possible to export some of the data to a latex table with:

.. testcode::

    import h_transport_materials as htm
    prop1 = htm.Diffusivity(1, 0.1)
    prop2 = htm.Solubility(2, 0.2, law="henry")
    
    group = htm.PropertiesGroup([prop1, prop2])
    print(group.to_latex_table())

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    \begin{center}
        \begin{tabular}{ c c c }

            Material & pre-exp. factor & Act. energy \\
             & $1.00\times 10^{0}\ \frac{\mathrm{m}^{2}}{\mathrm{s}}$ & 0.10 eV/particle \\        
             & $2.00\times 10^{0}\ \frac{\mathrm{particle}}{\left(\mathrm{Pa} \cdot \mathrm{m}^{3}\right)}$ & 0.20 eV/particle \\
        \end{tabular}
    \end{center}