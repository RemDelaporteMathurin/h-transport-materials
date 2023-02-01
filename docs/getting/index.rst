Getting Started
===============

Installation
------------

After `getting python <https://www.python.org/downloads/>`_, simply run:

.. code:: console

    pip install h-transport-materials

To install a specific version of HTM (here v0.9):

.. code-block:: console

    pip install h-transport-materials==0.9


Your first HTM script
---------------------

To make sure that everything works, try running:

.. plot::
   :include-source: true
    
    import matplotlib.pyplot as plt

    import h_transport_materials as htm

    tungsten_permeabilities = htm.permeabilities.filter(material=htm.TUNGSTEN)
    htm.plotting.plot(tungsten_permeabilities)
    plt.yscale("log")

