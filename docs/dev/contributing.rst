.. _contributing:

Contributing to HTM
===================

Contribution workflow
---------------------

- fork
- clone
- commit your changes
- push
- open a pull request
- wait for the review process

Add a property to an existing material
--------------------------------------

Rules for adding a property
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Check that the property doesn't already exist in the HTM database
- Only add published data

Best practices
^^^^^^^^^^^^^^

- use the units given by the author, minimise manual conversions
- whenever possible use the experimental data provided by the authors
- don't hesitate to add notes to the property using the ``note`` argument.

Experimental data
^^^^^^^^^^^^^^^^^

- either given by the authors in the paper (prefered). Add a reference to where the data is in the paper in ``note``.
- or numerise the plots with web plot digitizer and export it as csv

As transparency and reproductibility are part of our philosophy, please attach the WebPlotDigitizer project to HTM:

1. Download the project as a .tar archive File/SaveProject.

2. Move the .tar file to the appropriate folder inside `property_database/`

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


- when providing experimental data, no need to add a ``range`` value and the temperature range will be worked out from the experimental points.


Depending on how the .csv file is formatted, the python code should look like::

    data = np.genfromtxt(
        str(Path(__file__).parent) + "/oishi_1989_diffusivity.csv",
        delimiter=",",
        names=True,
    )

    property = Diffusivity(
        data_T=(1 / data["X"]) * htm.ureg.K,
        data_y=data["Y"] * htm.ureg.cm**2 * htm.ureg.s**-1,
        source="source",
    )

Reference
^^^^^^^^^

- Bibtex format


Adding a new material
---------------------


