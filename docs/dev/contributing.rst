.. _contributing:

Contributing to HTM
===================

Thank you for willing to contribute to HTM!
Any kind of contribution is most welcome, from bug reports, to fixes, enhancements, and also new features and new database entries.
This page describes the contribution workflow as well as the rules and best practices for contributing.

Anyone wishing to make contributions to HTM should be familiar with git and GitHub.
We assume you have git installed on your system, have a GitHub account, and are able to pull/push to repositories on GitHub.

Additionally, we assume you have `Python <https://www.python.org/downloads/>`_ and `pip <https://pip.pypa.io/en/stable/installation/>`_ installed.

Contribution workflow
---------------------

#. Fork the repository

First, create a fork of the repository.
This is a personnal copy of the repository where you can commit changes without interfering with other developers.

.. image:: https://user-images.githubusercontent.com/40028739/215575310-9b3eb090-1bf4-406e-9f90-bda5bf4d3c7b.png
    :alt: htm_repo_screenshot

#. Clone your fork and create a development branch::

    git clone https://github.com/your_username/h-transport-materials
    cd h-transport-materials
    git checkout -b newbranch

#. Make your changes. Make sure to :ref:`test your code<testing>`.

   Note: you can install your development version of HTM with::

       pip install -e .

#. Push and `open a pull request <https://github.com/RemDelaporteMathurin/h-transport-materials/compare>`_. The test suite will be run automatically.

#. One of the maintainers will review the pull request. Any potential issues with the pull request can be discussed directly here. If need be, simply commit new changes to your development branch to update the pull request.

Add a property
--------------

If you want to add a property of a material that doesn't already exist in the database, first :ref:`add the material <Adding a new material>`.

Rules for adding a property
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* The property doesn't already exist in the HTM database
* The property comes from a published source
* The property must have the following attributes:

  * Arrhenius parameters or experimental datapoints
  * a ``source``
  * an ``isotope``
  * a ``range`` (if it doesn't have experimental datapoints)
  * a ``material``

Best practices
^^^^^^^^^^^^^^

* Use the units given by the author, minimise manual conversions. See :ref:`user_units` for more information on units in HTM.

* Whenever possible use the experimental data provided by the authors. If for some reason it isn't possible, leave a ``note`` and/or a ``# TODO`` comment.

* Add anything relevant to the property with the ``note`` argument.

* If there is a discrepency in the original paper (for example: the equation and the plotted curve don't match):

  #. Use the datapoints
   
  #. Indicate the discrepency in ``note``


Experimental data
^^^^^^^^^^^^^^^^^

When providing experimental data, no need to add a ``range`` value: the temperature range will be worked out from the experimental points directly.

In papers, experimental datapoints are either given in a table, given in a graph, and rarely given as supplementary data files.

Given in a table in the paper
"""""""""""""""""""""""""""""

If the dataset is small, the data can be either copied to the python script.
Otherwise, the data can be stored in a CSV file and then read by the python script.
See below how to add a CSV file in HTM.

It is recommended to add a reference to where the data is in the paper in ``note`` (eg. ``"table 7"``).
This way, it is easy for users to find the origin of the data without having to read the whole paper::

    my_diff = Diffusivity(
        data_T=np.array([200, 300, 400, 500]) * htm.ureg.K,
        data_y=[1, 2, 3, 4] * htm.ureg.cm**2 * htm.ureg.s**-1,
        source="the_reference",
        note="data can be found in Table 7"
    )


From a graph
""""""""""""

If the data is only plotted on a graph, numerise the plots with `WebPlotDigitizer <https://apps.automeris.io/wpd/>`_ and export it as a CSV file.
As transparency and reproductibility are at the heart of the HTM philosophy, please attach the `WebPlotDigitizer <https://apps.automeris.io/wpd/>`_ project to HTM:

#. Download the project as a .tar archive File/SaveProject.

#. Move the .tar file to the appropriate folder inside ``property_database/``

#. If several subfolders were added, add a ``__init__.py`` file to all the subfolders to make them importable

The folder should look like::

    h_transport_materials/h_transport_materials
    | property_database
    | |  ...
    | | name_of_material
    | | | __init__.py
    | | | name_of_material.py
    | | | author_year.tar
    | | | property_data.csv

In the case where several WebPlotDigitizer projects are present::

    h_transport_materials/h_transport_materials
    | property_database
    | |  ...
    | | name_of_material
    | | | __init__.py
    | | | name_of_material.py
    | | | author_year
    | | | | __init__.py
    | | | | property1.tar
    | | | | property2.tar
    | | | | property1_data.csv
    | | | | property2_data.csv

Depending on how the .csv file is formatted, the python code should look like::

    data = np.genfromtxt(
        str(Path(__file__).parent) + "/oishi_1989_diffusivity.csv",
        delimiter=",",
        names=True,
    )

    my_diff = Diffusivity(
        data_T=(1 / data["X"]) * htm.ureg.K,
        data_y=data["Y"] * htm.ureg.cm**2 * htm.ureg.s**-1,
        source="the_reference",
    )

Given as a supplementary file
"""""""""""""""""""""""""""""

If the authors provide data as a supplementary file (rather uncommon), either download the file and put a copy in the appropriate folder then read directly from this file.
It is recommended to add a link to the data supplementary file for reproductibility sake. 

Reference
^^^^^^^^^

When adding a property, the reference should be given as a bibtex reference.
The reference should be citable and a DOI is preferred.
See :ref:`Add a reference` to see how to add a reference.

Material
^^^^^^^^

All the properties in the database must have a corresponding material.
See :ref:`Attach a material` to learn how to add a material to a property.
If the property material doesn't exist, refer to :ref:`Adding a new material`.

Adding a new material
---------------------

To add a material, go to ``h_transport_materials/material.py`` and create a new :class:`Material() <h_transport_materials.material.Material>` object.
Use the class appropriate to the material. For instance, when adding an alloy:

.. testcode::

    import h_transport_materials as htm

    MY_ALLOY = htm.Alloy("name_of_my_alloy")


When adding a pure metal:

.. testcode::

    MY_METAL = htm.PureMetal("name", "symbol")

By convention, the name of the variable for the :class:`Material() <h_transport_materials.material.Material>` should be capitalized.

Then, create a file in ``h_transport_materials/property_database`` with the name of the material (eg. ``tungsten.py``).
If need be, put this script in a folder with the name of the material (see :ref:`From a graph`).

The new material can then be added to the properties (see :ref:`Attach a material`).

Adding a feature
----------------

Before starting working on a new feature, reach out to the users and developers of HTM by `raising an issue <https://github.com/RemDelaporteMathurin/h-transport-materials/issues/new>`_.
Here we'll be able to discuss the implementation of this feature and maybe even improve the idea.

Then, follow the usual :ref:`Contribution workflow` and be sure to add a test that proves your feature works.
More info on python testing `here <https://realpython.com/python-testing/>`_.

Fixing a bug
------------

Before starting making changes to fix a bug, please `open an issue reporting the bug <https://github.com/RemDelaporteMathurin/h-transport-materials/issues/new>`_ (if there isn't one already).
To be as efficient as possible, the issue should contain a Minimal Working Example that reproduces the bug.

When fixing a bug, follow the usual :ref:`Contribution workflow` but add a test that catches the bug to prove that your fix is effective.
More info on python testing `here <https://realpython.com/python-testing/>`_.

.. _testing:

Testing your code
-----------------

Regardless the addition (contributing to the database, fixing a bug, adding a feature...), your code needs to be tested.
When you open a pull request, your code will automatically be tested by running the test suite.
The test suite can be found in the ``tests`` folder.

To test the local source code, run::

    pytest .

You may have to install the tests dependencies (like ``pytest``)::

    pip install -e .[tests]
