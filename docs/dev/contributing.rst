.. _contributing:

Contributing to HTM
===================

Contribution workflow
---------------------

1. Fork the repository

First, create a fork of the repository.
This is a personnal copy of the repository where you can commit changes without interfering with other developers.

.. image:: https://user-images.githubusercontent.com/40028739/215575310-9b3eb090-1bf4-406e-9f90-bda5bf4d3c7b.png
    :alt: htm_repo_screenshot

2. Clone your fork and create a development branch

.. code::
    git clone https://github.com/your_username/h-transport-materials
    cd h-transport-materials
    git checkout -b newbranch

3. Make your changes

4. Push and `open a pull request <https://github.com/RemDelaporteMathurin/h-transport-materials/compare>`_

5. One of the maintainers will review the pull request. Any potential issues with the pull request can be discussed directly here. If need be, simply commit new changes to your development branch to update the pull request.

Add a property to an existing material
--------------------------------------

Rules for adding a property
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Check that the property doesn't already exist in the HTM database
- Only add published data

Best practices
^^^^^^^^^^^^^^

- Use the units given by the author, minimise manual conversions. See :ref:`user_units` for more information on units in HTM.
- Whenever possible use the experimental data provided by the authors. If for some reason it isn't possible, leave a ``note`` and/or a ``# TODO`` comment.
- Add anything relevant to the property with the ``note`` argument.

Experimental data
^^^^^^^^^^^^^^^^^

When providing experimental data, no need to add a ``range`` value: the temperature range will be worked out from the experimental points directly.

In papers, experimental datapoints are either:

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

If the data is only plotted on a graph, numerise the plots with WebPlotDigitizer and export it as a CSV file.
As transparency and reproductibility are at the heart of the HTM philosophy, please attach the WebPlotDigitizer project to HTM:

1. Download the project as a .tar archive File/SaveProject.

2. Move the .tar file to the appropriate folder inside ``property_database/``

3. If several subfolders were added, add a ``__init__.py`` file to all the subfolders to make them importable

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

- Bibtex format


Adding a new material
---------------------


