import h_transport_materials as htm
import matplotlib.pyplot as plt
import numpy as np

my_D = htm.diffusivities.filter(material="copper")

mean_D_0, mean_E_D = my_D.mean()

for prop in my_D:
    htm.plotting.plot(prop)

D_mean = htm.ArheniusProperty(mean_D_0, mean_E_D)
htm.plotting.plot(D_mean, color="black", linewidth=3)

plt.yscale("log")
plt.show()
