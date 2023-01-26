Defining a property
===================

Arrhenius parameters
--------------------

Properties can be defined in HTM by using the :class:`ArrheniusProperty() <h_transport_materials.ArrheniusProperty>` class.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(pre_exp=1, act_energy=0.2)


.. TODO add test here!

More precise classes can also be used like :class:`Diffusivity() <h_transport_materials.Diffusivity>`, :class:`Solubility() <h_transport_materials.Solubility>`, :class:`Permeability() <h_transport_materials.Permeability>`, :class:`RecombinationCoeff() <h_transport_materials.RecombinationCoeff>`, :class:`DissociationCoeff() <h_transport_materials.DissociationCoeff>`.

.. testcode::

    from h_transport_materials import Diffusivity, Solubility, Permeability

    my_diff = Diffusivity(D_0=1, E_D=0.2)
    my_sol = Solubility(units="m-3 Pa-1/2", S_0=1, E_S=0.2)
    my_perm = Permeability(pre_exp=1, act_energy=0.2)

Temperature range
-----------------

A temperature range can be associated with a property.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(pre_exp=1, act_energy=0.2, range=(300, 400))

In this example, the property is defined over the 300-400 K temperature range (see :ref:`user_units` for more information on units).


Property from experimental data
-------------------------------

It is possible to define an :class:`ArrheniusProperty() <h_transport_materials.ArrheniusProperty>` directly from (T,y) points.
In this case, the Arrhenius parameters will be fitted automatically from the data points.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(
        data_T=[400, 500, 600, 700],
        data_y=[200, 300, 400, 500]
    )
    print(my_property)


Attach a material
-----------------

.. _user_units:

Units
-----

HTM uses pint to automatically converts units.
If no units are given, defaults units are assumed.
The units are stored in a `pint.UnitRegistry` that can be accessed by `h_transport_materials.ureg`.

.. testcode::

    from h_transport_materials import Diffusivity, ureg

    my_property = Diffusivity(
        D_0=1 * ureg.cm**2 * ureg.s**-1,
        E_D=20 * ureg.kJ * ureg.mol**-1,
    )

    print(my_property.pre_exp)
    print(my_property.act_energy)

.. testoutput::

    0.0001 meter ** 2 / second
    0.20728539312524347 electron_volt / particle

This is extremely useful when units start getting complicated:

.. testcode::

    from h_transport_materials import Permeability, ureg

    my_perm = Permeability(
        pre_exp=1 * ureg.mol * ureg.cm**-1 * ureg.hour**-1 * ureg.bar**-0.5,
        act_energy=20 * ureg.kcal * ureg.mol**-1,
    )

    print(my_property.pre_exp)
    print(my_property.act_energy)

.. testoutput::

    0.0001 meter ** 2 / second
    0.20728539312524347 electron_volt / particle

