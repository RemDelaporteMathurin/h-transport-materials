import matplotlib.pyplot as plt

import h_transport_materials as htm

tungsten_permeabilities = htm.permeabilities.filter(material=htm.TUNGSTEN)
htm.plotting.plot(tungsten_permeabilities)
plt.yscale("log")
plt.show()
