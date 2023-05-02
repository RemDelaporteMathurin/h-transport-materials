Defining a property
===================

Most - if not all - H transport properties are thermally activated. Meaning they follow the Arrhenius law:

:math:`X = X_0 \ \exp{\left( \frac{-E_X}{k_B \ T} \right)}`

Here, :math:`X_0` is called the pre-exponential factor and :math:`E_X` is the activation energy.
:math:`T` is the temperature and :math:`k_B` is the Boltzman constant.

The Arrhenius law is sometimes written as:
:math:`X = X_0 \ \exp{\left( \frac{-E_X}{R_g \ T} \right)}`
with :math:`R_g` the gas constant.

Note, :math:`R_g` and :math:`k_B` are linked by Avogadro's number :math:`N_A`.

:math:`R_g = N_A \ k_B`

Arrhenius parameters
--------------------

Properties can be defined in HTM by using the :class:`ArrheniusProperty() <h_transport_materials.property.ArrheniusProperty>` class.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(pre_exp=1, act_energy=0.2)


More precise classes can also be used like :class:`Diffusivity() <h_transport_materials.property.Diffusivity>`, :class:`Solubility() <h_transport_materials.property.Solubility>`, :class:`Permeability() <h_transport_materials.property.Permeability>`, :class:`RecombinationCoeff() <h_transport_materials.property.RecombinationCoeff>`, :class:`DissociationCoeff() <h_transport_materials.property.DissociationCoeff>`.

.. testcode::

    from h_transport_materials import Diffusivity, Solubility, Permeability

    my_diff = Diffusivity(D_0=1, E_D=0.2)
    my_sol = Solubility(S_0=1, E_S=0.2, law="henry")
    my_perm = Permeability(pre_exp=1, act_energy=0.2, law="sievert")

Note, :class:`Solubility() <h_transport_materials.property.Solubility>` has a `units` argument because depending on the material, the units can be m-3 Pa-1/2 (Sievert's law of solubility) or m-3 Pa-1 (Henry's law of solubility).

Temperature range
-----------------

A temperature range can be associated with a property.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(pre_exp=1, act_energy=0.2, range=(300, 400))

In this example, the property is defined over the 300-400 K temperature range (see :ref:`user_units` for more information on units).


Property from experimental data
-------------------------------

It is possible to define an :class:`ArrheniusProperty() <h_transport_materials.property.ArrheniusProperty>` directly from (T,y) points.
In this case, the Arrhenius parameters will be fitted automatically from the data points.

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(
        data_T=[400, 500, 600, 700],
        data_y=[200, 300, 400, 500]
    )
    print(my_property)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    Author:
    Material:
    Year: None
    Isotope: None
    Pre-exponential factor: 1.67×10³
    Activation energy: 7.34×10⁻² eV/particle


Attach a material
-----------------

A material can be attached to a property.
The simple case is to give the material as a string:

.. testcode::

    from h_transport_materials import ArrheniusProperty

    my_property = ArrheniusProperty(
        pre_exp=1,
        act_energy=0.2,
        material="tungsten"
    )

If the material already exists in the material database, the HTM object can be used instead:

.. testcode::

    from h_transport_materials import ArrheniusProperty, TUNGSTEN

    my_property = ArrheniusProperty(
        pre_exp=1,
        act_energy=0.2,
        material=TUNGSTEN
    )


.. _user_units:

Units
-----

HTM uses pint to automatically converts units.
If no units are given, defaults units are assumed.
The units are stored in a :class:`pint.UnitRegistry` that can be accessed by ``h_transport_materials.ureg``.

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

    print(my_perm.pre_exp)
    print(my_perm.act_energy)

.. testoutput::

    5.289911442149285e+19 particle / meter / pascal ** 0.5 / second
    0.8672820848360187 electron_volt / particle

Most attributes of properties in HTM are :class:`pint.Quantity` objects: pre-exponential factors, activation energies, temperature range.
Visit the `pint documentation <https://pint.readthedocs.io/en/stable/index.html>`_ to learn more.

Evaluate property at a given temperature
----------------------------------------

It is possible to evaluate the value of a property at a given temperature.

.. testcode::

    from h_transport_materials import Diffusivity, ureg

    D = Diffusivity(
        D_0=1 * ureg.cm**2 * ureg.s**-1,
        E_D=20 * ureg.kJ * ureg.mol**-1,
    )
    print(D.value(400 * ureg.K))

.. testoutput::

    2.4446573022139513e-07 meter ** 2 / second

To visualise the temperature dependency of an Arrhenius property, see :ref:`plotting_user`.


Add a reference
---------------

References are very important in order to track the origin of the property.
Three methods exist to add a reference to a property in HTM.

**Method 1:** Fields like ``author``, ``year``, and ``source`` can be added manually:

.. testcode::

    import h_transport_materials as htm

    D = htm.Diffusivity(
        D_0=1,
        E_D=0.2,
        author="Shrek",
        year=2023,
        source="name of book"
    )

**Method 2:** One can provide a source in the Bib format.

.. testcode::

    import h_transport_materials as htm

    bibsource = """@article{my_shrek_reference,
        title = {Name of Book},
        doi = {10.1016/awesome.journal.2023.1234},
        journal = {An Awesome Journal},
        author = {Shrek},
        year = {2023},
        pages = {1--2},
    }"""

    D = htm.Diffusivity(
        D_0=1,
        E_D=0.2,
        source=bibsource
    )

    print(D.author)
    print(D.year)
    print(D.doi)

.. testoutput::

    shrek
    2023
    10.1016/awesome.journal.2023.1234

**Method 3:** In the ``h_transport_materials`` directory, there is a ``references.bib`` file containing a most of the references of HTM.
One can also append the source in the Bib format to ``references.bib`` and then add the reference to ``source``.
The previous example would then be:

.. testcode::

    import h_transport_materials as htm

    D = htm.Diffusivity(
        D_0=1,
        E_D=0.2,
        source="my_shrek_reference"
    )

Add notes
---------

Sometimes it is useful to add custom notes to a property.

.. testcode::

    import h_transport_materials as htm

    D = htm.Diffusivity(
        D_0=1,
        E_D=0.2,
        note="this was measured under atmospheric pressure",
    )