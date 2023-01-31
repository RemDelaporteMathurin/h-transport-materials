Building the documentation
==========================

In order to build the documentation in the ``docs`` directory, you will need to have the `Sphinx <https://www.sphinx-doc.org/en/master/>`_ Python package.
The easiest way to install Sphinx is via pip:

.. code-block:: console

    pip install sphinx

Additionally, you will need several Sphinx extensions that can be installed
directly with pip:

.. code-block:: console

    pip install -r docs/requirements.txt

Build as a webpage
------------------

To build the documentation as a html webpage (what appears at https://h-transport-materials.readthedocs.io):

.. code:: console

    cd docs
    make.bat html

Test the documentation
----------------------

The code blocks and examples given in the documentation can be tested by running:

.. code:: console

    cd docs
    make.bat doctest
