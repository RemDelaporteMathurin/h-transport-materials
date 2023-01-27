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
