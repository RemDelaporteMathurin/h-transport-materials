import h_transport_materials as htm
import matplotlib.pyplot as plt

my_D = htm.diffusivities.filter(material="tungsten")

mean_D_0, mean_E_D = my_D.mean()

for prop in my_D:
    htm.plotting.plot(prop, alpha=0.5)

D_mean = htm.ArheniusProperty(mean_D_0, mean_E_D)
htm.plotting.plot(D_mean, color="black", linewidth=3)

x_annotation = 0.0034
plt.annotate("mean value", (x_annotation, D_mean.value(T=1 / x_annotation)))

plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
plt.yscale("log")
plt.show()
